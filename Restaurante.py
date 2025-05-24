class ItemMenu:
    def __init__(self, nombre, precio):
        self._nombre = nombre
        self._precio = precio
    
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, value):
        self._nombre = value
    
    @property
    def precio(self):
        return self._precio
    
    @precio.setter
    def precio(self, value):
        if value >= 0:
            self._precio = value
        else:
            raise ValueError("El precio no puede ser negativo")
    
    def calcular_total(self, cantidad=1):
        return self._precio * cantidad


class Bebida(ItemMenu):
    def __init__(self, nombre, precio, tamaño):
        super().__init__(nombre, precio)
        self._tamaño = tamaño
    
    @property
    def tamaño(self):
        return self._tamaño
    
    @tamaño.setter
    def tamaño(self, value):
        self._tamaño = value
    
    def calcular_total(self, cantidad=1):
        if self._tamaño.lower() == "grande":
            return self._precio * cantidad * 0.95
        return super().calcular_total(cantidad)


class Plato(ItemMenu):
    def __init__(self, nombre, precio, tipo):
        super().__init__(nombre, precio)
        self._tipo = tipo
    
    @property
    def tipo(self):
        return self._tipo
    
    @tipo.setter
    def tipo(self, value):
        self._tipo = value
    
    def calcular_total(self, cantidad=1):
        if self._tipo.lower() == "principal":
            return self._precio * cantidad * 0.90
        return super().calcular_total(cantidad)


class Postre(ItemMenu):
    def __init__(self, nombre, precio, tipo):
        super().__init__(nombre, precio)
        self._tipo = tipo
    
    @property
    def tipo(self):
        return self._tipo
    
    @tipo.setter
    def tipo(self, value):
        self._tipo = value
    
    def calcular_total(self, cantidad=1):
        return super().calcular_total(cantidad)


class Pedido:
    def __init__(self):
        self.items = []
    
    def agregar_item(self, item, cantidad=1):
        self.items.append((item, cantidad))
    
    def tiene_plato_principal(self):
        for item, _ in self.items:
            if isinstance(item, Plato) and hasattr(item, 'tipo'):
                if item.tipo.lower() == "principal":
                    return True
        return False
    
    def calcular_total(self):
        subtotal = 0
        tiene_principal = self.tiene_plato_principal()
        
        for item, cantidad in self.items:
            precio_item = item.calcular_total(cantidad)
            
            if tiene_principal and isinstance(item, Bebida):
                precio_item *= 0.95
            
            subtotal += precio_item
        
        descuento = subtotal * 0.1 if subtotal > 50 else 0
        impuesto = subtotal * 0.19
        total = subtotal - descuento + impuesto
        
        return {
            'subtotal': subtotal,
            'descuento': descuento,
            'impuesto': impuesto,
            'total': total
        }
    
    def mostrar_factura(self):
        print("\n=== FACTURA ===")
        for i, (item, cantidad) in enumerate(self.items, 1):
            print(f"{i}. {item.nombre} x{cantidad} - ${item.calcular_total(cantidad):.2f}")
        
        totales = self.calcular_total()
        print("\nRESUMEN:")
        print(f"Subtotal: ${totales['subtotal']:.2f}")
        if totales['descuento'] > 0:
            print(f"Descuento (10%): -${totales['descuento']:.2f}")
        print(f"IVA (19%): +${totales['impuesto']:.2f}")
        print(f"TOTAL: ${totales['total']:.2f}")
        print("================")


class Pago:
    def __init__(self, pedido, metodo="efectivo"):
        self.pedido = pedido
        self.metodo = metodo
        self.monto = pedido.calcular_total()['total']
        self.estado = "pendiente"
    
    def procesar_pago(self):
        import random
        exito = random.random() > 0.1  
        
        if exito:
            self.estado = "completado"
            return True
        self.estado = "fallido"
        return False
    
    def generar_recibo(self):
        print("\n--RECIBO DE PAGO--")
        print(f"Método de pago: {self.metodo}")
        print(f"Total pagado: ${self.monto:.2f}")
        print(f"Estado: {self.estado}")
        


if __name__ == "__main__":
    
    refresco = Bebida("Refresco de los amigos de al lado", 2.50, "mediano")
    cerveza = Bebida("Cerveza/Cachaza", 4.00, "grande")
    ensalada = Plato("Ensalada Felipe ;)", 6.50, "entrada")
    pizza = Plato("Pizza", 12.00, "principal")
    baby_beef = Plato("Baby beef", 20.00, "principal")
    banana_split = Postre("Banana split", 5.00, "postre")
    
    
    pedido = Pedido()
    pedido.agregar_item(refresco, 2)
    pedido.agregar_item(cerveza)
    pedido.agregar_item(ensalada)
    pedido.agregar_item(pizza, 2)
    pedido.agregar_item(baby_beef)
    pedido.agregar_item(banana_split)
    
    pedido.mostrar_factura()
    
    pago = Pago(pedido, "tarjeta")
    if pago.procesar_pago():
        print("\n¡Pago exitoso!")
    else:
        print("\n¡Error en el pago!")
    pago.generar_recibo()
