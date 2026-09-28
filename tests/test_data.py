INVALID_REGISTRATION = [
    ("different_pass", "diff_pass@test.com", "Password123!", "Diff_Password123!", "20", "Пароли не совпадают"),
    ("short_pass", "short_pass@test.com", "Pa1", "Pa1", "20", "Пароль не соответствует требованиям"),
    ("12345678", "username_without_letters@test.com", "Password123!", "Password123!", "20", "Логин должен начинаться с буквы, содержать только латиницу/цифры/_ и быть длиной 3–20 символов"),
    ("L1", "short_username@test.com", "Password123!", "Password123!", "20", "Логин должен начинаться с буквы, содержать только латиницу/цифры/_ и быть длиной 3–20 символов")
]

PROMO_CODES = [
    ("SAVE20", True),
    ("WELCOME10", True),
    ("INVALID_CODE", False)
]