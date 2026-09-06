from .models import model

result = model.invoke(
    "Hello! Who are you? Briefly introudce yourself"
)

print(result.content)
