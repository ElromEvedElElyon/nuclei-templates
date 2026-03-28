# Ollama Security Findings — huntr.com Submission Package
# Em nome do Senhor Jesus Cristo
# Date: 27 Mar 2026
# Target: ollama/ollama (latest main branch)
# Researcher: ElromSecurity / inteligenciaartificial.now@gmail.com

---

## FINDING 1 [HIGH — $4,000]: GGUF V1 String Panic via Zero-Length String

**File**: `fs/ggml/gguf.go` lines 296-311
**Type**: Denial of Service (Crash)
**CWE**: CWE-129 (Improper Validation of Array Index)

### Description
`readGGUFV1String()` reads a string length as uint64, then calls `io.CopyN(&b, r, int64(length))`. If `length == 0`, CopyN copies 0 bytes, leaving `b.Len() == 0`. The subsequent `b.Truncate(b.Len() - 1)` evaluates to `b.Truncate(-1)`, which panics because Go's `bytes.Buffer.Truncate` panics on negative arguments.

### Vulnerable Code
```go
func readGGUFV1String(llm *gguf, r io.Reader) (string, error) {
    var length uint64
    if err := binary.Read(r, llm.ByteOrder, &length); err != nil {
        return "", err
    }
    var b bytes.Buffer
    if _, err := io.CopyN(&b, r, int64(length)); err != nil {
        return "", err
    }
    b.Truncate(b.Len() - 1) // PANIC when length=0: Truncate(-1)
    return b.String(), nil
}
```

### PoC
Craft a minimal GGUF V1 file where any string field (key name, value, or tensor name) has `length = 0x0000000000000000`. When Ollama parses this file via `ollama pull`, `ollama create`, or `ollama show`, the server process panics and crashes.

### Impact
Server crash (DoS). Any user who downloads or imports a crafted GGUF V1 model file will crash their Ollama instance.

### Fix
Add bounds check: `if b.Len() == 0 { return "", nil }` before the Truncate call.

---

## FINDING 2 [HIGH — $4,000]: Unbounded Tensor Dimensions Allocation (OOM)

**File**: `fs/ggml/gguf.go` lines 200-212
**Type**: Denial of Service (OOM Crash)
**CWE**: CWE-789 (Memory Allocation with Excessive Size Value)

### Description
Tensor dimension count (`dims`) is read as uint32 from the GGUF file with no upper bound check. GGUF spec limits dimensions to 4 (GGML_MAX_DIMS=4), but the code does `make([]uint64, dims)` without validation. Setting `dims = 0xFFFFFFFF` attempts to allocate ~32GB, causing OOM crash.

### Vulnerable Code
```go
dims, err := readGGUF[uint32](llm, rs)
// NO bounds check: dims can be 0 to 4,294,967,295
shape := make([]uint64, dims) // OOM for large dims
```

### PoC
Craft GGUF file with valid header, `numTensor >= 1`, set first tensor's dimension field to `0xFFFFFFFF`. Server crashes with OOM on parse.

### Fix
Add `if dims > 4 { return error }` matching GGML_MAX_DIMS.

---

## FINDING 3 [HIGH — $4,000]: Unbounded String Allocation in GGUF V2/V3 Parsing

**File**: `fs/ggml/gguf.go` lines 348-372
**Type**: Denial of Service (OOM/Panic)
**CWE**: CWE-789 (Memory Allocation with Excessive Size Value)

### Description
`readGGUFString()` reads string length as uint64, converts to int. If `length > scratch_size`, allocates `make([]byte, length)` with no upper bound. Crafted file with `length = 0x7FFFFFFFFFFFFFFF` causes multi-exabyte allocation attempt (OOM). If `length = 0xFFFFFFFFFFFFFFFF`, `int(length)` becomes -1, causing `llm.scratch[:-1]` panic (negative slice index).

### Vulnerable Code
```go
length := int(llm.ByteOrder.Uint64(buf)) // uint64->int: can be negative
if length > len(llm.scratch) {
    buf = make([]byte, length) // OOM for large values
} else {
    buf = llm.scratch[:length] // PANIC for negative values
}
```

### Impact
Server crash via any GGUF V2/V3 string field.

---

## FINDING 4 [HIGH — $4,000]: Safetensors Header Size OOM

**File**: `convert/reader_safetensors.go` lines 36-41
**Also**: `x/imagegen/safetensors/safetensors.go` lines 34-39
**Type**: Denial of Service (OOM)
**CWE**: CWE-789

### Description
Safetensors header size is read as int64/uint64 from the file's first 8 bytes with no upper bound validation. `make([]byte, headerSize)` with crafted `headerSize = 0x7FFFFFFFFFFFFFFF` causes immediate OOM.

### Vulnerable Code
```go
// reader_safetensors.go
var n int64
binary.Read(f, binary.LittleEndian, &n)
b := bytes.NewBuffer(make([]byte, 0, n)) // NO bounds check

// safetensors.go
var headerSize uint64
binary.Read(f, binary.LittleEndian, &headerSize)
headerBytes := make([]byte, headerSize) // NO bounds check
```

### Fix
Add maximum header size check (e.g., 100MB).

---

## FINDING 5 [HIGH — $4,000]: Integer Overflow in Tensor Size Calculations

**File**: `fs/ggml/ggml.go` lines 504-514
**Type**: Integer Overflow / Bounds Check Bypass
**CWE**: CWE-190

### Description
`Elements()` multiplies all tensor dimensions without overflow detection. With crafted dimensions like `[0xFFFFFFFF, 0xFFFFFFFF]`, the result wraps around. `Size()` (which uses `Elements()`) then overflows to a small value, bypassing the file size bounds check at line 259. Downstream code sees original large dimensions, leading to out-of-bounds reads.

### Vulnerable Code
```go
func (t Tensor) Elements() uint64 {
    var count uint64 = 1
    for _, n := range t.Shape {
        count *= n // NO overflow check
    }
    return count
}
```

---

## FINDING 6 [HIGH — $4,000]: discardGGUFString Signed Integer Overflow

**File**: `fs/ggml/gguf.go` lines 330-345
**Type**: Parser Desynchronization
**CWE**: CWE-681

### Description
`discardGGUFString()` converts uint64 size to int. Values >= 0x8000000000000000 become negative. The `for size > 0` loop never executes, returning without reading expected bytes. This desynchronizes the parser, causing subsequent reads to interpret random data as GGUF structures.

### Vulnerable Code
```go
size := int(llm.ByteOrder.Uint64(buf)) // negative for high bit set
for size > 0 { // NEVER executes for negative size
    n, err := r.Read(llm.scratch[:min(size, cap(llm.scratch))])
    size -= n
}
return nil // returns success without reading anything
```

---

## FINDING 7 [HIGH — $1,500]: BashTool RCE via Prompt Injection

**File**: `x/tools/bash.go` lines 53-114
**Type**: Remote Code Execution
**CWE**: CWE-78

### Description
The BashTool executes arbitrary shell commands via `exec.CommandContext(ctx, "bash", "-c", command)` with no sandboxing, allowlisting, or path restrictions. If a malicious prompt injection occurs (via crafted model system prompts, user inputs, or tool-use responses), arbitrary OS commands execute as the Ollama process user.

### Vulnerable Code
```go
func (b *BashTool) Execute(args map[string]any) (string, error) {
    command, ok := args["command"].(string)
    // ... NO sanitization, NO allowlist, NO sandbox ...
    cmd := exec.CommandContext(ctx, "bash", "-c", command) // DIRECT EXEC
```

---

## FINDING 8 [MEDIUM — $1,500]: DNS Rebinding Host Header Bypass

**File**: `server/routes.go` lines 1571-1596
**Type**: Authentication Bypass
**CWE**: CWE-350

### Description
`allowedHost()` accepts any hostname ending in `.local`, `.internal`, or `.localhost`. An attacker can register `evil.localhost` or `attacker.internal` pointing to 127.0.0.1, bypassing host validation to access the API from a malicious webpage.

---

## FINDING 9 [MEDIUM — $1,500]: TLS Bypass via https+insecure Scheme

**File**: `server/internal/client/ollama/registry.go` lines 969-995
**Type**: Man-in-the-Middle
**CWE**: CWE-295

### Description
The `https+insecure` URL scheme disables TLS certificate verification. User-supplied model names are parsed for scheme at line 1165-1177. A user can be tricked into `ollama pull "https+insecure://evil.com/llama3"` which downloads without certificate validation.

---

## FINDING 10 [MEDIUM — $1,500]: No API Authentication on Non-Loopback

**File**: `server/routes.go` lines 1598-1634
**Type**: Missing Authentication
**CWE**: CWE-306

### Description
When configured with `OLLAMA_HOST=0.0.0.0`, the `allowedHostsMiddleware` skips ALL host validation. Combined with zero API authentication, any network client can create/delete models, generate completions, upload blobs, and exhaust disk/GPU resources.

---

## FINDING 11 [HIGH — $1,500]: unsafe.Slice Buffer Over-Read in Quantization

**File**: `server/quantization.go` lines 40-43
**Type**: Buffer Over-Read
**CWE**: CWE-125

### Description
`unsafe.Slice` creates a Go slice using `q.from.Elements()` which is computed from attacker-controlled GGUF tensor dimensions. If dimensions overflow, `Elements()` can produce a value larger than actual data buffer, creating a slice extending beyond heap allocation.

---

## SUMMARY

| # | Finding | Severity | Category | Est. Bounty |
|---|---------|----------|----------|-------------|
| 1 | GGUF V1 String Panic | HIGH | Model File | $4,000 |
| 2 | Tensor Dims OOM | HIGH | Model File | $4,000 |
| 3 | String Allocation OOM/Panic | HIGH | Model File | $4,000 |
| 4 | Safetensors Header OOM | HIGH | Model File | $4,000 |
| 5 | Tensor Size Integer Overflow | HIGH | Model File | $4,000 |
| 6 | discardGGUFString Desync | HIGH | Model File | $4,000 |
| 7 | BashTool RCE | HIGH | Other | $1,500 |
| 8 | DNS Rebinding | MEDIUM | Other | $1,500 |
| 9 | TLS Bypass | MEDIUM | Other | $1,500 |
| 10 | No Auth Non-Loopback | MEDIUM | Other | $1,500 |
| 11 | Quantization Over-Read | HIGH | Other | $1,500 |

**TOTAL POTENTIAL: $31,500**
