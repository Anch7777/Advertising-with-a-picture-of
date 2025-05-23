# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pdb  # Для отладки

# Список элементов в памяти
items = []
next_id = 1  # Глобальный счетчик для генерации уникальных ID

class ItemView(APIView):
    def get(self, request):
        """
        Получить список всех элементов.
        """
        return Response(items)

    def post(self, request):
        """
        Создать новый элемент.
        - Поле "name" обязательно.
        - Поле "description" необязательно.
        """
        global next_id

        # Добавляем точку останова для отладки
        pdb.set_trace()

        # Получаем данные из тела запроса
        data = request.data

        # Проверяем, что поле "name" существует и не пустое
        name = data.get("name")
        if not name:
            return Response(
                {"error": "Field 'name' is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Создаем новый элемент с уникальным ID
        new_item = {
            "id": next_id,
            "name": name,
            "description": data.get("description", ""),  # Описание не обязательно
        }
        items.append(new_item)
        next_id += 1  # Увеличиваем счетчик ID

        # Возвращаем созданный элемент
        return Response(new_item, status=status.HTTP_201_CREATED)

    def put(self, request):
        """
        Обновить существующий элемент по ID.
        - Поле "id" обязательно.
        - Можно обновить "name" и/или "description".
        """
        # Получаем данные из тела запроса
        data = request.data

        # Проверяем, что поле "id" существует
        item_id = data.get("id")
        if not item_id:
            return Response(
                {"error": "Field 'id' is required for update"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ищем элемент по ID
        for item in items:
            if item["id"] == item_id:
                # Обновляем поля "name" и "description"
                if "name" in data:
                    item["name"] = data["name"]
                if "description" in data:
                    item["description"] = data["description"]
                return Response(item, status=status.HTTP_200_OK)

        # Если элемент не найден
        return Response(
            {"error": f"Item with id={item_id} not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    def delete(self, request):
        """
        Удалить элемент по ID.
        - Поле "id" обязательно.
        """
        # Получаем данные из тела запроса
        data = request.data

        # Проверяем, что поле "id" существует
        item_id = data.get("id")
        if not item_id:
            return Response(
                {"error": "Field 'id' is required for deletion"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ищем элемент по ID
        for item in items:
            if item["id"] == item_id:
                items.remove(item)
                return Response(
                    {"message": f"Item with id={item_id} deleted"},
                    status=status.HTTP_204_NO_CONTENT
                )

        # Если элемент не найден
        return Response(
            {"error": f"Item with id={item_id} not found"},
            status=status.HTTP_404_NOT_FOUND
        )