def eliminate_dead_code(code):
    expressions = set()
    cleaned_code = []
    cod1 = code.split('\n')
    for line in cod1:
        l1 = ''.join(line.strip().split(" "))
        l2,l3 = l1.split("=")
        l = []
        
    return '\n'.join(cleaned_code)

def eliminate_redundant_subexpressions(code):
    expressions = set()
    cleaned_code = []
    cod1 = code.split('\n')
    cod1 = cod1[::-1]
    for line in cod1:
        l1 = ''.join(line.strip().split(" "))
        l2,l3 = l1.split("=")
        if l3 not in expressions:
            cleaned_code.append(line)
            expressions.add(l3)
    return '\n'.join(cleaned_code)

def main():
    input_code = "x = 5 + 3\ny = 2 + 3\nz = 5 + 3\nw = 2 + 3"

    print("Original code:")
    print(input_code)

    cleaned_code = eliminate_dead_code(input_code)
    print("\nAfter eliminating dead code:")
    print(cleaned_code)

    cleaned_code = eliminate_redundant_subexpressions(cleaned_code)
    print("\nAfter eliminating redundant subexpressions:")
    print(cleaned_code)

if __name__ == "__main__":
    main()
