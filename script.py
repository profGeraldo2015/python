#segunda_pessoa = input("Digite o nome da segunda pessoa: ")
#print(f"Olá, {segunda_pessoa}! Bem-vindo ao nosso programa.")

one_person = [
    {
        "nome": "Geraldo",
        "idade": 30,
    },
    {
        "nome": "Maria",
        "idade": 25,
    }
]

print(f"Nome: {one_person[0]['nome']}, Idade: {one_person[0]['idade']}")
print(f"Nome: {one_person[1]['nome']}, Idade: {one_person[1]['idade']}")

for person in one_person:
    print(f"Nome2: {person['nome']}, Idade2: {person['idade']}")