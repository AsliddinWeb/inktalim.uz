#!/usr/bin/env python3
"""
Admin foydalanuvchi yaratish skripti.

Ishlatish:
    # Docker ichida:
    docker compose exec backend python create_admin.py

    # Yoki argumentlar bilan:
    docker compose exec backend python create_admin.py \
        --email admin@example.com \
        --phone +998901234567 \
        --name "Super Admin" \
        --password MySecret123
"""

import argparse
import asyncio
import sys
import uuid

from sqlalchemy import select


async def main(email: str, phone: str, full_name: str, password: str) -> None:
    # Import bu yerda — skript app kontekstida ishlaganda ishlaydi
    from app.database import AsyncSessionLocal
    from app.models.user import User
    from app.models import course, lesson, module, progress  # noqa: F401
    from app.core.security import hash_password

    # Parol minimal uzunlik tekshiruvi
    if len(password) < 8:
        print("❌ Parol kamida 8 ta belgidan iborat bo'lishi kerak.")
        sys.exit(1)

    async with AsyncSessionLocal() as db:
        # Email yoki telefon band emasligini tekshirish
        existing = await db.execute(
            select(User).where(
                (User.email == email) | (User.phone == phone)
            )
        )
        user = existing.scalar_one_or_none()

        if user:
            if user.email == email:
                print(f"❌ '{email}' email allaqachon ro'yxatdan o'tgan.")
            else:
                print(f"❌ '{phone}' telefon allaqachon ro'yxatdan o'tgan.")
            sys.exit(1)

        new_admin = User(
            id=uuid.uuid4(),
            email=email,
            phone=phone,
            full_name=full_name,
            hashed_password=hash_password(password),
            is_admin=True,
            is_active=True,
        )
        db.add(new_admin)
        await db.commit()
        await db.refresh(new_admin)

    print("✅ Admin muvaffaqiyatli yaratildi!")
    print(f"   ID       : {new_admin.id}")
    print(f"   Ism      : {new_admin.full_name}")
    print(f"   Email    : {new_admin.email}")
    print(f"   Telefon  : {new_admin.phone}")
    print(f"   is_admin : {new_admin.is_admin}")
    print(f"   is_active: {new_admin.is_active}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Admin foydalanuvchi yaratish")
    parser.add_argument(
        "--email",
        default="asliddinsinger@gmail.com",
        help="Admin email manzili (default: asliddinsinger@gmail.com)",
    )
    parser.add_argument(
        "--phone",
        default="+998942025511",
        help="Telefon raqami +998XXXXXXXXX formatida (default: +998942025511)",
    )
    parser.add_argument(
        "--name",
        default="Super Admin",
        dest="full_name",
        help="To'liq ism (default: Super Admin)",
    )
    parser.add_argument(
        "--password",
        default="Admin123456",
        help="Parol, kamida 8 belgi (default: Admin123456)",
    )

    args = parser.parse_args()

    print("🚀 Admin yaratilmoqda...")
    print(f"   Email  : {args.email}")
    print(f"   Telefon: {args.phone}")
    print(f"   Ism    : {args.full_name}")
    print()

    asyncio.run(main(
        email=args.email,
        phone=args.phone,
        full_name=args.full_name,
        password=args.password,
    ))
