# RETO_04POO
Ejercicio de clase de figuras y mejora del codigo del restaurante :b

## EXPLICACION (Ejercicio de clase)
### Class point
- Se obtiene cordenadas x, y en un plano 2D
- Tiene el metodo restart para poner las coordenadas en 0,0

### Class line
- Representa una linea que une a unos puntos sea x1, y1 hasta x2, y2

### Class SHAPE
- Clase base abstracta para todas las formas.
- Define interfaz común con métodos que deben implementar las subclases.
- Incluye posición central

### Class square
- Una figura que representa que ancho = alto hechas desde las coordenadas x1, y1 x2, y2

### Class rectangle
- Implementa un rectángulo con ancho y alto.
- Calcula esquinas, área, perímetro.
- Detecta interferencia con puntos y líneas.

### Class triangle
- Genera un triangulo generico
- Calcula que tipo de triangulo es

## EXPLICACION (Ejercicio Restaurante) CHANGELOG
- Se agregaron los setter y getters a lo largo del menu
- Se realizo una clase de pago el cual simula uno real con un proceso y resultados hipoteticos como pago fallido en proceso o exitoso sin afectar el funcionamiento del codigo (Decorativo)
- Se añadio un sistema de descuento acorde al plato principal y su bebida



