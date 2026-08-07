from pprint import pprint
import csv, re


with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
pprint(contacts_list)


def format_phone(phone):
  # Удаляем всё, кроме цифр и "доб"
  cleaned = re.sub(r"[^+\dдоб]", "", phone)

  # Ищем основной номер: 11 цифр, начинающихся с 7 или 8
  main_match = re.search(r"(\d{11})", cleaned)
  if not main_match: return ""  
  digits = main_match.group(1)
  # Приводим к +7...
  if digits.startswith("8"): digits = "7" + digits[1:]
  elif not digits.startswith("7"): return ""

  # 3. Форматируем основной номер
  formatted = f"+7({digits[1:4]}){digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
    
  # 4. Добавочный (ищем в ОРИГИНАЛЬНОЙ строке, чтобы не потерять "доб")
  ext_match = re.search(r"доб\.?(\d+)", phone)
  if ext_match:
    formatted += f" доб.{ext_match.group(1)}"
    
  return formatted

# Обработка контактов
contacts_dict = {}

def create_contact(contact_list):
# Проходим по всем строкам, кроме заголовка
  for contact in contact_list[1:]:
      # Нормализуем ФИО
      parts = " ".join(contact[:3]).split()
      lastname = parts[0] if len(parts) > 0 else ""
      firstname = parts[1] if len(parts) > 1 else ""
      surname = parts[2] if len(parts) > 2 else ""
      
      # Остальные поля
      org = contact[3]
      pos = contact[4]
      phone = format_phone(contact[5])
      email = contact[6]
      
      key = (lastname, firstname)

      if key not in contacts_dict:
          contacts_dict[key] = [lastname, firstname, surname, org, pos, phone, email]
      else:
          # Объединяем записи: заполняем пустые поля
          existing = contacts_dict[key]
          existing[2] = existing[2] or surname
          existing[3] = existing[3] or org
          existing[4] = existing[4] or pos
          existing[5] = existing[5] or phone
          existing[6] = existing[6] or email
      return [contacts_list[0]] + list(contacts_dict.values())


with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(create_contact(contacts_list))

print("Готово! Результат сохранён в phonebook.csv")