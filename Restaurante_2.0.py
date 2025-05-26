class ItemMenu:
    def __init__(self, nombre, precio):
        self._nombre = nombre
        self._precio = precio
    
    def get_nombre(self):
        return self._nombre
    
    def set_nombre(self, value):
        if isinstance(value, str) and value.strip():
            self._nombre = value.strip()
        else:
            raise ValueError("El nombre debe ser un texto no vacío")
    
    def get_precio(self):
        return self._precio
    
    def set_precio(self, value):
        if isinstance(value, (int, float)) and value >= 0:
            self._precio = round(value, 2)
        else:
            raise ValueError("El precio debe ser un número positivo")
    
    def calcular_total(self, cantidad=1):
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero positivo")
        return self._precio * cantidad


class Bebida(ItemMenu):
    def __init__(self, nombre, precio, tamaño):
        super().__init__(nombre, precio)
        self.set_tamaño(tamaño)
    
    def get_tamaño(self):
        return self._tamaño
    
    def set_tamaño(self, value):
        tamanos_validos = ["pequeño", "mediano", "grande"]
        if isinstance(value, str) and value.lower() in tamanos_validos:
            self._tamaño = value.lower()
        else:
            raise ValueError(f"Tamaño inválido. Opciones: {', '.join(tamanos_validos)}")
    
    def calcular_total(self, cantidad=1):
        super().calcular_total(cantidad)  
        if self._tamaño == "grande":
            return round(self._precio * cantidad * 0.95, 2)  
        return round(self._precio * cantidad, 2)


class Plato(ItemMenu):
    def __init__(self, nombre, precio, tipo):
        super().__init__(nombre, precio)
        self.set_tipo(tipo)
    
    def get_tipo(self):
        return self._tipo
    
    def set_tipo(self, value):
        tipos_validos = ["entrada", "principal", "acompañamiento"]
        if isinstance(value, str) and value.lower() in tipos_validos:
            self._tipo = value.lower()
        else:
            raise ValueError(f"Tipo inválido. Opciones: {', '.join(tipos_validos)}")
    
    def calcular_total(self, cantidad=1):
        super().calcular_total(cantidad)  
        if self._tipo == "principal":
            return round(self._precio * cantidad * 0.90, 2)  
        return round(self._precio * cantidad, 2)


class Postre(ItemMenu):
    def __init__(self, nombre, precio, tipo="postre"):
        super().__init__(nombre, precio)
        self.set_tipo(tipo)
    
    def get_tipo(self):
        return self._tipo
    
    def set_tipo(self, value):
        if isinstance(value, str) and value.lower() in ["postre", "especial"]:
            self._tipo = value.lower()
        else:
            raise ValueError("Tipo de postre inválido")


class Pedido:
    def __init__(self):
        self._items = []
    
    def get_items(self):
        return self._items.copy()  
    
    def agregar_item(self, item, cantidad=1):
        if not isinstance(item, ItemMenu):
            raise ValueError("El item debe ser del menú")
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero positivo")
        
        
        for i, (existing_item, existing_cantidad) in enumerate(self._items):
            if existing_item.get_nombre() == item.get_nombre():
                self._items[i] = (item, existing_cantidad + cantidad)
                return
        
        self._items.append((item, cantidad))
    
    def eliminar_item(self, nombre_item, cantidad=1):
        for i, (item, item_cantidad) in enumerate(self._items):
            if item.get_nombre() == nombre_item:
                if cantidad >= item_cantidad:
                    del self._items[i]
                else:
                    self._items[i] = (item, item_cantidad - cantidad)
                return
        raise ValueError("Item no encontrado en el pedido")
    
    def tiene_plato_principal(self):
        for item, _ in self._items:
            if isinstance(item, Plato) and item.get_tipo() == "principal":
                return True
        return False
    
    def calcular_total(self):
        subtotal = 0.0
        tiene_principal = self.tiene_plato_principal()
        
        for item, cantidad in self._items:
            precio_item = item.calcular_total(cantidad)
            
            
            if tiene_principal and isinstance(item, Bebida):
                precio_item = round(precio_item * 0.95, 2)
            
            subtotal += precio_item
        
        
        descuento = round(subtotal * 0.1, 2) if subtotal > 50 else 0.0
        impuesto = round(subtotal * 0.19, 2)  
        total = round(subtotal - descuento + impuesto, 2)
        
        return {
            'subtotal': subtotal,
            'descuento': descuento,
            'impuesto': impuesto,
            'total': total
        }
    
    def mostrar_factura(self):
        print("\n=== FACTURA ===")
        for i, (item, cantidad) in enumerate(self._items, 1):
            nombre = item.get_nombre()
            precio = item.calcular_total(cantidad)
            print(f"{i}. {nombre} x{cantidad} - ${precio:.2f}")
        
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
        if not isinstance(pedido, Pedido):
            raise ValueError("Se requiere un pedido válido")
        
        self._pedido = pedido
        self.set_metodo(metodo)
        self._monto = pedido.calcular_total()['total']
        self._estado = "pendiente"
    
    def get_metodo(self):
        return self._metodo
    
    def set_metodo(self, value):
        metodos_validos = ["efectivo", "tarjeta", "transferencia"]
        if isinstance(value, str) and value.lower() in metodos_validos:
            self._metodo = value.lower()
        else:
            raise ValueError(f"Método de pago inválido. Opciones: {', '.join(metodos_validos)}")
    
    def get_monto(self):
        return self._monto
    
    def get_estado(self):
        return self._estado
    
    def procesar_pago(self):
        import random
        exito = random.random() > 0.1  
        
        if exito:
            self._estado = "completado"
            return True
        
        self._estado = "fallido"
        return False
    
    def generar_recibo(self):
        print("\n--RECIBO DE PAGO--")
        print(f"Método de pago: {self._metodo}")
        print(f"Total pagado: ${self._monto:.2f}")
        print(f"Estado: {self._estado}")
        if self._estado == "completado":
            print("¡Gracias por su compra!")
        else:
            print("Por favor intente nuevamente")


if __name__ == "__main__":
    try:
        
        refresco = Bebida("Refresco", 2.50, "mediano")
        cerveza = Bebida("Cerveza", 4.00, "grande")
        ensalada = Plato("Ensalada", 6.50, "entrada")
        pizza = Plato("Pizza", 12.00, "principal")
        baby_beef = Plato("Baby beef", 20.00, "principal")
        banana_split = Postre("Banana split", 5.00)
        
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
    
    except ValueError as e:
        print(f"\nError: {e}")