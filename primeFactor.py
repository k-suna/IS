import ast
import time
import math

start = time.time()
print("実行時間計測開始")

#試し割り法による素因数分解の計算
def prime_factors(n):
    factors = []
    i = 2
    while i * i <= n:
        if (n%i != 0): #nがiで割り切れないとき→素因数ではない
            i += 1
        else: #nがiで割り切れたとき→素因数の発見＆nをそれで割ったときの商の値に更新
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    factors_no_dup = list(set(factors)) #重複した素因数を削除
    factors_list = sorted(factors_no_dup) #素因数を昇順に並び替え
    return factors_list

with open('C:/Users/skait/Desktop/graduated_subject/IS/Ns.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    data = ast.literal_eval(content)
    key = 66112300334
    composite_num_list = data[key] #素因数分解すべき合成数Nの集合
    for count, composite_num in enumerate(composite_num_list[:25]):
        factors = prime_factors(composite_num)
        print(f"{count+1}．「{composite_num}」を素因数分解すると「{factors[0]} * {factors[1]}」です.")

end = time.time() - start
print("*---------------------------------*")
print(f"{count+1}個の計算に{math.floor(end)}秒かかりました．")