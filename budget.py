class Category:
    def __init__(self, category):
        self.category = category
        self.ledger = []
        self.balance = 0

    def __str__(self):
        str_rep = self.__get_title()

        for entry in self.ledger:
            amount = '{:7.2f}'.format(entry['amount'])[0:7]
            desc = str(entry['description'])[0:23]

            if len(desc) < 23:
                while len(desc) < 23:
                    desc += ' '
            
            str_rep += '\n' + desc + amount

        str_rep += '\n' + 'Total: ' + '{:1.2f}'.format(self.balance)

        return str_rep

    def __get_title(self):
        max_char = 30
        title = ''

        for i in range(0, max_char // 2 - len(self.category) // 2):
            title += '*'

        title += self.category

        while len(title) < max_char:
            title += '*'

        return title

    def deposit(self, amt, desc=''):
        self.balance += amt
        self.ledger.append({ 'amount': amt, 'description': desc })

    def check_funds(self, amt):
        return self.balance >= amt

    def withdraw(self, amt, desc=""):
        if not self.check_funds(amt):
            return False

        amt_minus = amt * -1
        self.balance += amt_minus
        self.ledger.append({ 'amount': amt_minus, 'description': desc })
        return True

    def get_balance(self):
        return self.balance

    def transfer(self, amt, destination):
        if not self.check_funds(amt):
            return False

        self.withdraw(amt, f'Transfer to {destination.category}')
        destination.deposit(amt, f'Transfer from {self.category}')
        return True


def create_histogram(category_list):
    histogram = dict()

    for category in category_list:
        for entry in category.ledger:
            name = category.category
            if entry['amount'] < 0:
                histogram[name] = histogram.get(name, 0) + entry['amount']
                histogram['total'] = histogram.get('total', 0) + entry['amount']
    
    return histogram

def create_spend_chart(category_list):
    histogram = create_histogram(category_list)
    y_axis = (100, 90, 80, 70, 60, 50, 40, 10, 0, -10)
    graph = ''


    for step in y_axis:
        if step >= 0:
            graph += '{:3}'.format(step) + '|'
            for category in category_list:
                name = category.category
                percentage = round(100 / histogram['total'] * histogram[name])

                if percentage >= step:
                    graph += ' o '
                else:
                    graph += '   '
        else:
            graph += '    '
            for category in category_list:
                graph += '---'
        graph += '\n'

    index = 0
    while True:
        names_complete = True
        graph += '    '
        for category in category_list:
            name = category.category
            
            if index >= len(name):
                graph += '   '
                names_complete = names_complete and True
            else:
                graph += ' ' + name[index] + ' '
                names_complete = False

        if names_complete: 
            break

        graph += '\n'
        index += 1


    return graph