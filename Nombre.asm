.model small
.stack 100h
.data
   mensaje db "Sergio Andres Reay Arero,ID:1028864919$"

.code 
main proc
    mov ax, @data
    mov ds, ax

    mov ah, 09h
    lea dx, mensaje
    int 21h

    mov ah, 4Ch
    int 21h
main endp
end main
