section .text
global _start

_start:
    ; Get the CPU ID information using CPUID
    mov rax, 0x80000001          ; syscall number for CPUID
    xor rcx, rcx                 ; ECX = 0 (instruction pointer)
    syscall

    ; Print the CPU ID information
    mov rsi, rsp
    mov rdx, 16                  ; length of the CPU ID information
    mov rax, 1                   ; write to stdout
    mov rdi, 1                   ; file descriptor for stdout
    syscall

section .data
cpu_id_info times 16 db 0