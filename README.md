# Airbnb project

## 2024.10.30

### setting

1. create app

2. create admin model

### All Models

- Users
  - Profile Photo
  - Gender
  - Language
  - Currency Options
- Rooms
  - Country
  - City
  - Price Per Night
  - Description
  - Owner
  - Room #
  - Toilet #
  - Address
  - Pet Friendly
  - Category
  - Type of Place (Entire Place|Private Room|Shared Room)
- Amenities (Many to Many)
  - Name
- Experiences
  - Country
  - City
  - Name
  - Host
  - Price
  - Description
  - Address
  - Start Time
  - End Time
  - Category
- Materials (Many to Many)
  - Name
  - Description
- Categories
  - Kind (Room|Experience)
  - Name
- Reviews
  - Review
  - Rating
  - Room
  - Experience
  - User
- Wishlists
  - Name
  - Rooms
  - Experiences
  - User
- Bookings
  - Kind (Room|Experience)
  - Room
  - Experience
  - Check In
  - Check Out
  - Experience Date
- Photos
  - File
  - Description
  - Room
  - Experience
- Messages

  - Room
    - Users
  - Message

    - Text
    - User
    - Room

  -

## 2024.10.31

### Custom Model, Forign Keys

1. Custom Model and Abstract Classes

- Django 기본 사용자 모델을 커스텀하기 위해 `AbstractUser` 클래스를 상속하여 Custom Model을 정의

```python
# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Custom fields can be added here
    pass
```

2. Foreign Keys

- Foreign Key 필드는 다른 모델과의 관계를 설정
- `on_delete` 옵션에 `models.CASCADE`를 사용하여 참조된 객체가 삭제될 때 연결된 객체도 함께 삭제

```python
owner = models.ForeignKey(
    "users.User",
    on_delete=models.CASCADE,
)
```

3. Non-nullable Fields

- `Custom` 모델에서 필드에 `default` 값을 설정하여 non-nullable 제약 조건을 피할

```python
name = models.CharField(max_length=150, default="",)
```

4. Error Handling: OperationalError 해결

- 개발환경에서는 `migratons`와 `db.sqlite3`를 삭제
- 다시 마이그레이션 실행

## 2024.11.02

### All Model Update

## 2024.11.05

### Power Admin: Search Fields, Admin Actions, Custom Filters

1. Search Fields

- 목적: admin 패널에서 특정 필드르 기준으로 검색 기능 제공
- 사용법: `search_fields` 옵션에 원하는 필드를 추가

```python
search_fields = (
  "name",
  "^prcie",               # price로 시작하는 값을 찾음
  "=owner__username",     # 정확히 일치하는 owner username을 찾음
)
```

2. Admin Actions

- 목적: 선택된 객체에 대해 일괄적인 작업 수행
- 사용법: `@admin.action` 데코레이터를 사용하여 특정 동작을 정의하고, 이를 admin 패널에서 액션으로 선택 가능하게 만듦

```python
@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, rooms):
  for room in rooms.all():
    room.price = 0
    room.save()
```

3. Custom Filters

- 목적: 데이터의 특정 필드를 기준으로 필터링 옵션을 제공
- 사용법: `SimpleListFilter`를 상속하여 필터 클래스를 작성하고, `lookups`와 `queryset`메서드를 정의

  1. `lookups`

  - 역할: admin 패널의 필터링 인터페이스에 표시될 옵션 목록을 정의
  - 동작
    - 첫 번째 값은 **데이터베스에 전달되는 값**이고,
    - 두 번쨰 값은 **admin 패널에서 사용자에게 표시될 이름**

  ```python
  def lookups(self, request, model_admin):
    return [
        ("good", "Good"),    # 선택하면 "good"이라는 값이 DB에 전달되고, 화면에는 "Good"으로 표시됨
        ("great", "Great"),
        ("awesome", "Awesome"),
    ]
  ```

  2. querset

  - 역할: `lookups`에서 선택한 **필터 옵션에 따라 데이터베이스에서 필터링된 쿼리셋을 반환**
  - 동작: 사용자가 특정 필터 옵션을 선택하면, `queryset` 메서드가 해당 값을 이용해 필터링 작업을 수행
    - `self.value()` 는 현재 선택된 옵션의 값을 가짐

  ```python
  def queryset(self, request, reviews):
    word= self.value()         # 선택된 필터의 값, 예: "good"
    if word:
      return reviews.filter(payload__contains=word) # 선택된 값이 포함된 데이터를 필터링
    else:
      return reviews
  ```

#### Summary

`lookups`는 필터 옵션을 정의하고, `queryset`은 필터링된 데이터를 반환

## 2024.11.06

### Django URL Routing and Views

1. URL Patterns (config/urls.py)

- 목적: Django에서 URL 라우팅을 통해 특정 URL로 요청이 들어올 때 지정한 view로 연결하는 역할
- 사용법: `path()` 함수로 URL과 view 함수를 연결하며, `include()` 함수로 다른 앱의 URL 설정을 포함

```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("rooms/", include("rooms.urls")),  # rooms 앱의 URL을 포함
]
```

2. Rooms URL Configuration (rooms/urls.py)

- 목적: rooms 앱의 각 URL이 어떤 view로 연결될지 정의
- 사용법: `path()` 함수와 정수형 매개변수 (`<int:room_pk>`)를 통해 특정 방의 세부 정보로 이동할 수 있도록 함.

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.see_all_rooms),            # 모든 방을 표시하는 뷰 연결
    path("<int:room_pk>", views.see_one_room),  # 특정 방의 세부 정보를 표시하는 뷰 연결
]
```

3. Views (views.py)

- 목적: 클라이언트의 요청에 대해 실제 데이터베이스를 조회하거나 처리 후 결과를 템플릿과 함께 반환.

- 사용법: render() 함수를 사용하여 템플릿을 렌더링하며, 예외 처리를 통해 방이 존재하지 않는 경우 적절한 응답을 반환.

```python
from django.shortcuts import render
from django.http import HttpResponse
from .models import Room
```

- 뷰 함수:
  - `see_all_rooms`: 모든 방의 목록을 조회하여 `all_rooms.html` 템플릿에 전달

```python
def see_all_rooms(request):
    rooms = Room.objects.all()
    return render(
        request,
        "all_rooms.html",
        {
            "rooms": rooms,
            "title": "Hello! this title comes from django!",
        },
    )
```

- `see_one_room`: 특정 방의 세부 정보를 조회하여 `room_detail.html`에 전달하며, 방이 없는 경우 '`not_found`' 변수를 템플릿에 전달.

```python
def see_one_room(request, room_pk):
    try:
        room = Room.objects.get(pk=room_pk)
        return render(
            request,
            "room_detail.html",
            {
                "room": room,
            },
        )
    except Room.DoesNotExist:
        return render(
            request,
            "room_detail.html",
            {
                "not_found": True,
            },
        )
```

## 2024.11.07

### Django REST Framework API Views and Serializers

1. @api_view 데코레이터

- 목적: HTTP 메서드에 따라 다른 로직을 실행할 수 있도록 뷰 함수에 허용되는 HTTP 메서드를 지정함. 예를 들어, ["GET", "POST"]를 사용하여 해당 뷰가 GET과 POST 요청을 처리하도록 지정
- 사용법: `@api_view()` 데코레이터로 지정하고, 메서드를 리스트로 전달

```python
@api_view(["GET", "POST"])
def categories(request):
    # GET과 POST 요청을 처리하는 로직
```

2. CategorySerializer

- 목적: `Category` 모델의 인스턴스를 JSON 형식으로 직렬화하고, 역직렬화를 통해 데이터를 검증하고 저장. 이를 통해 API에서 JSON 데이터를 다루기 쉽게 만듦
- 사용법: `serializers.Serializer` 클래스를 상속받아 필드를 정의하고, `create`와 `update`메서드를 구현해 객체를 생성하고 업데이트

```python
class CategorySerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=50)
    kind = serializers.ChoiceField(choices=Category.CategoryKindChoices.choices)
    created_at = serializers.DateTimeField(read_only=True)
```

3. NotFound 예외 처리

- 목적: 요청한 리소스가 존재하지 않을 경우, 404 Not Found 응답을 반환하여 클라이언트가 요청한 자원이 없음을 알림

```python
try:
    category = Category.objects.get(pk=pk)
except Category.DoesNotExist:
    raise NotFound
```

4. Response 클래스

- 목적: HTTP 응답을 생성하며, JSON 형식의 데이터를 쉽게 반환할 수 있도록 도움. Response 객체를 사용해 클라이언트에게 데이터를 JSON 형태로 응답함.
- 사용법: Response(data) 형식으로 데이터를 전달하며, 응답 상태 코드를 추가함

```python
return Response(serializer.data)
```

## 2024.11.08

### Django REST Framework ModelViewSet and ModelSerializer

1. ModelViewSet

- 목적: 기본적인 CRUD 기능을 제공하는 ViewSet으로, 여러 HTTP메서드에 따라 자동으로 적절한 메서드를 실행해주며, 코드 간결성을 높임. `ModelViewSet`을 사용하여 CRUD 작업을 자동으로 처리
- 사용법: `ModelViewSet` 클래스를 상속받아 `serializer_class`와 `querset`을 정의함으로써 기본 CRUD 기능 제공

```python
from rest_framework.viewsets import ModelViewSet
from .models import Category
from .serializers import CategorySerializer

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
```

2. ModelSerializer

- 목적: 모델 인스턴스를 직렬화하고, 역직렬화하여 데이터를 검증 및 저장할 수 있도록 하며, `ModelSerializer`를 통해 모든 필드를 쉽게 직렬화할 수 있음
- 사용법: `serializers.ModelSerializer` 클래스를 상속받아 `Meta`, 클래스를 통해 모델과 필드를 지정하여 모든 필드를 직렬화

```python
from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
```

3. URL 라우팅

- 목적: 특정 URL 패턴을 통해 HTTP 메서드에 따라 동작을 지정하고, `ModelViewSet`을 사용하여 CRUD 작업을 간결하게 연결
- 사용법: `as_view` 메서드를 사용해 URL 패턴과 HTTP 메서드가 실행할 동작을 지정함

```python
from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.CategoryViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "<int:pk>",
        views.CategoryViewSet.as_view(
            {
                "get": "retrieve",
                "put": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
]
```
