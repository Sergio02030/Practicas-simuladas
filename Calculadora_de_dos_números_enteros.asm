.model small
.stack 100h
.data
   mensaje db "Ingrese el primer dato:$"
   mensaje1 db "Ingrese el segundo dato:$"
.code
main proc
    mov ax,@data
    mov ds,ax

    mov ah,09h
    lea dx,mensaje
    int 21h

    mov ah,01h
    int 21h
    

    mov ax,4Ch
    int 21h
main endp
end main
