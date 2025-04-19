#!/bin/bash

# Script para hacer git add, commit y push

# Verifica que se haya proporcionado un mensaje de commit
if [ "$#" -ne 1 ]; then
    echo "Uso: $0 \"mensaje del commit\""
    exit 1
fi

MENSAJE=$1

# Ejecuta los comandos de Git
git add --all
git commit -m "$MENSAJE"
git push origin main

# Verifica si el push fue exitoso
if [ $? -eq 0 ]; then
    echo "✅ Cambios subidos correctamente a GitHub"
else
    echo "❌ Error al subir los cambios"
fi