import json


def save_contact(user_id, fullname, phone_number):
    book_contact = {"user_id": user_id, "fullname": fullname, "phone_number": phone_number}
    with open(f'storage_contacts/{fullname}.json', mode='w', encoding="utf-8") as json_file:
        json.dump(book_contact, json_file)
