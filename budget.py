class Category:
  def __init__(self, name):
    self.name = name
    self.ledger = []

  def deposit(self, amount, description = ''):
    dep = {
      
      "amount": amount,
      "description": description.strip()
    }
    self.ledger.append(dep)
  
  def withdraw(self, amount, description = ''):
    success_balance = self.check_funds(amount)
    if success_balance:
      
      dep = {
        "amount": - amount,
        "description": description
      }
      self.ledger.append(dep)
      return True
    else:
      return False

  def get_balance(self):
    current_balance = 0
    if len(self.ledger) > 0:
      for i in range(len(self.ledger)):
        item = self.ledger[i]
        current_balance += item['amount']
      return current_balance
    else:
      return 0

  def get_total_used(self):
    current_balance = 0
    if len(self.ledger) > 0:
      for i in range(len(self.ledger)):
        item = self.ledger[i]
        if item['amount'] < 0:
          current_balance += item['amount']
      return abs(current_balance)
    else:
      return 0
    
    
  
  def transfer(self,amount, categoryObj):
    success = self.withdraw(amount, f"Transfer to {categoryObj.name}")
    if success:
      categoryObj.deposit(amount, f"Transfer from {self.name}")
      return True
    else:
      return False
  
  def check_funds(self, amount):
    current_balance = self.get_balance()
    if current_balance - amount >= 0:
      return True
    else:
      return False
  

  def create_print_header(self):
    maxLineLen = 30
    name = self.name
    name_len = len(name)
    if name_len > 23:
      name = name[0:23]
    
    name_len = len(name)

    star_len = maxLineLen - name_len

    stars = ''
    for i in range(round(star_len/2)):
      stars += '*'
    
    return stars + name + stars

  def create_print_line(self, description, amount):
    description_len = len(description)
    if description_len > 23:
      description = description[0:23]
    totalLetterLength = len(description + str(amount))
    maxLineLen = 30
    spaceNeeded = maxLineLen - totalLetterLength

    space = ''
    for i in range(spaceNeeded):
      space += ' '
    return description + space + str(amount)


  def get_transaction_string(self):
    log = ''
    for i in range(len(self.ledger)):
        item = self.ledger[i]
        description = str(item['description'])
        amount = ("{:.2f}".format(item['amount']))
        line = self.create_print_line(description, amount) 

        log += line + '\n'
    return log

  def __str__(self):
    header = self.create_print_header()
    log = self.get_transaction_string()
    current_balance = self.get_balance()
    return header + '\n' + log + 'Total: ' + str(current_balance)

############

def persentage_line_check(index,cat_dict):
  lines = ''
  persentage = (10 - index) * 10
  
  range_len = len(cat_dict)
  for i in range(range_len):
    cat_persentage = cat_dict[i]['persentage']
    set_point = cat_persentage >= persentage
    if set_point:
      lines += 'o  '
    else:
      lines += '   '
  return lines


def persentage_text(index):
  persentage = (10 - index) * 10
  if persentage == 100:
    return str(persentage) + '| '
  elif persentage == 0:
    return "  " +  str(persentage) + '| '
  else:
    return " " +  str(persentage) + '| '

def perssentage_chart(cat_dict):
  lines = ''
  for i in range(11):
    lines += persentage_text(i) + persentage_line_check(i,cat_dict) + '\n'
    
  return lines

def info_chart(cat_dict, max_name_length):
  lines = ''
  for i in range(max_name_length):
    line = '     '
    dict_len = len(cat_dict)
    for j in range(dict_len): 
      name = cat_dict[j]['name']
      if len(name) > i:
        letter = name[i]
        line +=  letter
        if j < dict_len - 1:
          line +=  '  '
        else:
          line +=  '  '
      else:
        line += '   '
    lines += line + '\n'
  return "     " + lines.strip() + "  "

def create_spend_chart(categories):
  totalAmount = 0
  cat_dict = []
  max_name_length = 0
  cat_len = len(categories)
  for i in range(cat_len):
    categorie = categories[i]
    balance = categorie.get_total_used()
    totalAmount += balance
    if len(categorie.name) > max_name_length:
      max_name_length = len(categorie.name)

    cat_dict.append({
      'amount': balance,
      'name': categorie.name
    })

  for i in range(len(cat_dict)):
    amount = cat_dict[i]['amount']
    persentage = amount/totalAmount * 100
    cat_dict[i]['persentage'] = round(persentage)

  lines = perssentage_chart(cat_dict)
  line_break = '   ----------\n'
  if len(cat_dict) == 3:
    line_break = '    ----------\n'

  names = info_chart(cat_dict, max_name_length)

  return 'Percentage spent by category\n' + lines + line_break + names