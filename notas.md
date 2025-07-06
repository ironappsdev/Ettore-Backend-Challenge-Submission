# Notas

## Decisiones
- Se decidió agregar como contexto a las consultas del modelo de LLM el perfil del usuario y los últimos 7 días de mediciones para que el modelo pueda generar recomendaciones personalizadas, pero con un tope de 20 mediciones para no sobrecargar el modelo y regular el uso de tokens.
- Debido al límite de tiempo, no alcancé a investigar los valores médicos correctos para el threshold helper. En lugar de dejar umbrales arbitrarios que funcionaran técnicamente pero carecieran de sentido médico, utilicé un LLM para completar la implementación con valores realistas que consideran el perfil del paciente (edad, género, condiciones preexistentes) y una primitiva normalización de unidades de medida. Prioricé entregar algo médicamente coherente antes que valores placeholder arbitrarios.


## Mejoras futuras
- Validar correctamente los datos de entrada
  - Solo se validan por tipo según el models pero no que estos tengan sentido en el contexto de la aplicación
- Agregar rate limit a los endpoints con LLM
- Crear pruebas unitarias para las distintas partes del código
- Hacer un helper de threshold configurable para que pueda ser afinado por expertos.
- Nuevamente, por tiempo, no pude afinar y mejorar los prompts así que esto queda pendiente.
- Utilizar exceptions más descriptivos y agregar los faltantes, ya que se utilizaron de manera muy generica.
- Terminar las notificaciones con mensajes personalizados y contextualizados al problema que las origina.
- Guardar los task id de celery para hacer seguimiento y retornarlos al usuario para que pueda consultar su estado