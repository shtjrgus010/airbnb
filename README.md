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
