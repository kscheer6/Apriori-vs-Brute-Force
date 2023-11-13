import pandas as pd
import time

start_time = time.process_time()

print('Please select a database numbered 1-5.\n'
      'Input an integer between 1 and 5\n'
      'Input 1 for Transaction Database 1.\n'
      'Input 2 for Transaction Database 2.\n'
      'Input 3 for Transaction Database 3.\n'
      'Input 4 for Transaction Database 4.\n'
      'Input 5 for Transaction Database 5.')


def load_dataset():
    y = input()
    while True:
        if y == "1":
            transactions = pd.read_csv(r"Transactions1.csv")
            transactionlist = transactions.values.tolist()
            print('You selected Transaction Database 1.\n')
            return transactionlist
        elif y == "2":
            transactions = pd.read_csv(r"Transactions2.csv")
            transactionlist = transactions.values.tolist()
            print('You selected Transaction Database 2.\n')
            return transactionlist
        elif y == "3":
            transactions = pd.read_csv(r"Transactions3.csv")
            transactionlist = transactions.values.tolist()
            print('You selected Transaction Database 3.\n')
            return transactionlist
        elif y == "4":
            transactions = pd.read_csv(r"Transactions4.csv")
            transactionlist = transactions.values.tolist()
            print('You selected Transaction Database 4.\n')
            return transactionlist
        elif y == "5":
            transactions = pd.read_csv(r"Transactions5.csv")
            transactionlist = transactions.values.tolist()
            print('You selected Transaction Database 5\n')
            return transactionlist
        else:
            print('Please select a database numbered 1-5.')
            break


transactionsloaded = load_dataset()
transactions = [[ele for ele in y if pd.isnull(ele) == False] for y in transactionsloaded]
number_of_transactions = len(transactions)

print("Please input your desired minimum support as an integer.")


def set_minimum_support():
    y = input()
    while True:
        if int(y) <= 100 and int(y) >= 1:
            minimumsupport = (int(y))/100
            print("You selected {}% as your minimum support value.\n".format(y))
            break
        else:
            print("Please input a valid integer")
            break
    return minimumsupport


minimumsupport = set_minimum_support()

print("Please input your desired minimum confidence as an integer.")


def set_minimum_confidence():
    y = input()
    while True:
        if int(y) <= 100 and int(y) >= 1:
            minimumconfidence = (int(y))/100
            print("You selected {}% as your minimum confidence value.\n".format(y))
            break
        else:
            print("Please input a valid integer")
            break
    return minimumconfidence


minimumconfidence = set_minimum_confidence()


def sort_transaction(transactions):
    transactionlist = []
    for t in transactions:
        t.sort()
        transactionlist.append(t)
    return transactionlist


transactionlist = sort_transaction(transactions)
itemslist = [i for j in transactionlist for i in j]
itemslist.sort()
items = []
[items.append(x) for x in itemslist if x not in items]
items.sort()


def counting(itemset, transactionlist):
    count = 0
    for q in range(len(transactionlist)):
        if set(itemset).issubset(set(transactionlist[q])):
            count += 1
    return count


def frequency(itemsets, transactionlist, minimumsupport, discarded):
    all_frequent_itemsets = []
    supp_count = []
    new_dc = []
    k = len(discarded)
    for i in range(len(itemsets)):
        discarded_already = False
        if k > 0:
            for dc in discarded[k]:
                if set(dc).issubset(set(itemsets[i])):
                    discarded_already = True
                    break
        if not discarded_already:
            count = counting(itemsets[i], transactionlist)
            if count/number_of_transactions >= minimumsupport:
                all_frequent_itemsets.append(itemsets[i])
                supp_count.append(count)
            else:
                new_dc.append(itemsets[i])
    return all_frequent_itemsets, supp_count, new_dc


candidates = {}
all_frequent_itemsets = {}
itemset_length = 1
discard = {itemset_length : []}
candidates.update({itemset_length : [ [x] for x in items]})
support_frequent = {}
freq_itemsets, support, new_discarded = frequency(candidates[itemset_length], transactionlist, minimumsupport, discard)
discard.update({itemset_length : new_discarded})
all_frequent_itemsets.update({itemset_length : freq_itemsets})
support_frequent.update({itemset_length : support})


def more_itemsets(itemsets, items):
    candidates = []
    for i in range(len(itemsets)):
        for j in range(i+1, len(itemsets)):
            def even_more_itemsets(can1, can2, items):
                can1.sort(key=lambda x: items.index(x))
                can2.sort(key=lambda x: items.index(x))
                for i in range(len(can1) - 1):
                    if can1[i] != can2[i]:
                        return []
                if items.index(can1[-1]) < items.index(can2[-1]):
                    return can1 + [can2[-1]]
                return []
            it_output = even_more_itemsets(itemsets[i], itemsets[j], items)
            if len(it_output) > 0:
                candidates.append(it_output)
    return candidates


def Apriori(candidates, transactionlist, minimumsupport, discard):
    l = itemset_length + 1
    more_candidates = True
    while more_candidates:
        candidates.update({l : more_itemsets(all_frequent_itemsets[l-1], items)})
        frequent_itemsets, support, new_discarded = frequency(candidates[l], transactionlist, minimumsupport, discard)
        discard.update({l : new_discarded})
        all_frequent_itemsets.update({l : frequent_itemsets})
        support_frequent.update({l : support})
        if len(all_frequent_itemsets[l]) == 0:
            more_candidates = False
        l += 1


def combinations(iter):
    s = list(iter)
    result = [[]]
    for x in s:
        result = result + [c + [x] for c in result]
        result2 = [ele for ele in result if ele != []]
    return result2


def writing_rules(freq, remainder, subset, confidence, support_freq, number_of_transactions):
    rules_output = ""
    rules_output += "Frequent Itemset: {}\n".format(freq)
    rules_output += " Support: {0:2.3f} \n".format(support_freq / number_of_transactions)
    rules_output += " Rule: {} -> {} \n".format(list(subset), list(remainder))
    rules_output += "  Confidence: {0:2.3f} \n\n".format(confidence)
    return rules_output


def Apriori_Association_Rules(all_frequent_itemsets, minimumconfidence, minimumsupport):
    association_rules = "\n\n"
    for i in range(1, len(all_frequent_itemsets)):
        for j in range(len(all_frequent_itemsets[i])):
            subset = list(combinations(set(all_frequent_itemsets[i][j])))
            subset.pop()
            for element in subset:
                subset = set(element)
                freq = set(all_frequent_itemsets[i][j])
                remainder = set(freq-subset)
                support_freq = counting(freq, transactionlist)
                support_remainder = counting(remainder, transactionlist)
                confidence = support_freq / support_remainder
                if confidence >= minimumconfidence and support_freq >= minimumsupport:
                    association_rules += writing_rules(freq, remainder, subset, confidence, support_freq, number_of_transactions)
    return association_rules


FI = all_frequent_itemsets[1]
IS2 = support_frequent[1]
IS = [x / number_of_transactions for x in IS2]


def writing_frequent_items_and_support(FI, IS):
    output = ""
    for i in range(0, (len(FI))):
        output += "Frequent Item: {}\n".format((FI[i]))
        output += " Support: {0:2.3f}\n\n".format((IS[i]))
    return output


def brute_frequency(itemsets, transactionlist, minimumsupport):
    brute_freq = []
    brute_support_count = []
    for i in range(len(itemsets)):
        count = counting(itemsets[i], transactionlist)
        if count/number_of_transactions >= minimumsupport:
            brute_freq.append(itemsets[i])
            brute_support_count.append(count)
    return brute_freq, brute_support_count


brute_candidates = {}
brute_all_frequent_itemsets = {}
brute_itemset_length = 1
brute_support_frequent = {}
brute_candidates.update({brute_itemset_length : [ [x] for x in items]})
brute_freq, brute_support_count = brute_frequency(brute_candidates[brute_itemset_length], transactionlist, minimumsupport)
brute_all_frequent_itemsets.update({brute_itemset_length : brute_freq})
brute_support_frequent.update({brute_itemset_length : brute_support_count})


def Brute_Force(brute_candidates, transactionlist, minimumsupport):
    r = brute_itemset_length + 1
    more_brute_candidates = True
    while more_brute_candidates:
        brute_candidates.update({r : more_itemsets(brute_all_frequent_itemsets[r-1], items)})
        brute_frequent_itemsets, brute_supp_count = brute_frequency(brute_candidates[r], transactionlist, minimumsupport)
        brute_all_frequent_itemsets.update({r : brute_frequent_itemsets})
        brute_support_frequent.update({r : brute_supp_count})
        if len(brute_all_frequent_itemsets[r]) == 0:
            more_brute_candidates = False
        r += 1


BFI = brute_all_frequent_itemsets[1]
BIS2 = brute_support_frequent[1]
BIS = [x / number_of_transactions for x in BIS2]


def Brute_Force_Association_Rules(brute_all_frequent_itemsets, minimumconfidence, minimumsupport):
    brute_association_rules = "\n\n"
    for i in range(1, len(brute_all_frequent_itemsets)):
        for j in range(len(brute_all_frequent_itemsets[i])):
            brute_subset = list(combinations(set(brute_all_frequent_itemsets[i][j])))
            brute_subset.pop()
            for elem in brute_subset:
                brute_subset = set(elem)
                brute_freq = set(brute_all_frequent_itemsets[i][j])
                brute_remainder = set(brute_freq - brute_subset)
                brute_support_freq = counting(brute_freq, transactionlist)
                brute_support_remainder = counting(brute_remainder, transactionlist)
                brute_confidence = brute_support_freq / brute_support_remainder
                if brute_confidence >= minimumconfidence and brute_support_freq >= minimumsupport:
                    brute_association_rules += writing_rules(brute_freq, brute_remainder, brute_subset, brute_confidence, brute_support_freq, number_of_transactions)
    return brute_association_rules


print("Please select how you would like to obtain the association rules.\n"
      "Input A to use Apriori algorithm\n"
      "Input B to use the brute force method")


def method():
    y = input()
    while True:
        if y == "A" or y == "a":
            print("You selected the Apriori method.\n Results are listed below.\n")
            Apriori(candidates, transactionlist, minimumsupport, discard)
            association_rules = Apriori_Association_Rules(all_frequent_itemsets, minimumconfidence, minimumsupport)
            FIS = writing_frequent_items_and_support(FI, IS)
            print(FIS, association_rules)
            break
        elif y == "B" or y == "b":
            print("You selected the brute force method.\n Results are listed below.\n")
            Brute_Force(brute_candidates, transactionlist, minimumsupport)
            brute_association_rules = Brute_Force_Association_Rules(brute_all_frequent_itemsets, minimumconfidence, minimumsupport)
            BFIS = writing_frequent_items_and_support(BFI, BIS)
            print(BFIS, brute_association_rules)
            break
        else:
            print("Please input either A or B to select a valid method.")


method()
et = time.process_time()
elapsed_time = et - start_time

print('Using this method took', elapsed_time, 'seconds.')
