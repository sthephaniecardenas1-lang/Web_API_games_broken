# Respuestas del parcial

1. ¿Qué error encontraste en la validación de `stock`?

En `schemas/game.py` el campo `stock` tenía `Field(ge=0, le=50)`, o sea que dejaba pasar el 0. La regla pide de 1 a 50, así que cambié el límite inferior a `ge=1`. Ahora el JSON de "Celeste" con `stock: 0` da 422. Esa validación la hace el schema, antes de que la petición llegue al service.

2. ¿Qué hacía que un juego pareciera creado pero no quedara persistido?

En `create_game` (service) se hacía `session.add(game)` y enseguida `session.refresh(game)`, pero faltaba el `session.commit()` en medio. Sin commit el INSERT nunca se confirma en `arcade.db`, y además `refresh()` fallaba porque el juego todavía no existía en la base (error `not persistent within this Session`, que se veía como un 500). Lo arreglé con el orden `add` → `commit` → `refresh`.

3. ¿Qué problema tenía el endpoint que lista juegos?

En el router tenía `response_model=GameResponse`, que describe un solo juego, pero `list_games` devuelve varios. FastAPI intentaba validar la lista como si fuera un único objeto y fallaba (`ResponseValidationError`, un 500). Lo cambié a `response_model=list[GameResponse]`.

4. ¿Cómo solucionaste la consulta de un ID inexistente?

`get_game` devolvía directamente `session.get(Game, game_id)`, que da `None` cuando el ID no existe, y el endpoint intentaba convertir ese `None` en un `GameResponse` (otro 500). Ahora el service revisa `if not game` y lanza `HTTPException(status_code=404, detail="Game not found")`, igual que ya hacía `delete_game`.

5. ¿Por qué DELETE podía responder correctamente y aun así no eliminar el registro de SQLite?

Porque `session.delete(game)` solo marca el objeto para borrarlo dentro de la sesión; el borrado no queda guardado hasta que se hace `session.commit()`. Sin el commit, la función igual devolvía `{"message": "Game deleted"}`, pero la transacción no se confirmaba y el juego seguía en `arcade.db`. Agregué `session.commit()` después del `delete`.

---

Pruebas ejecutadas y resultados: `evidencias/pruebas-curl.txt` (20 pruebas aprobadas, incluido el reinicio de Uvicorn para comprobar la persistencia).
