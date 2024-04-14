import ast
import time
import math

start = time.time() #開始時刻を取得する．
print("実行時間計測開始")

#整数a,b (a < b)の最大公約数を求める．
#「ユークリッドの互除法」を使用．
def gcd(a, b):
    while a:
        a, b = b%a, a
    return b

#与えられた自然数が素数かどうかを判定する．
#「ミラー・ラビン素数判定法」を使用．
def is_prime(n):
    if n == 2:     # n=2は素数なので，true(=1)を返す．
        return 1
    if n == 1 or n%2 == 0: # n=1や2で割り切れる数n（偶数）は素数ではないので，false(=0)を返す．
        return 0

    m = n - 1
    lsb = m & -m # 整数mをビット表現した時，最下位ビットの位置を取り出す．出力値は10進数である．（論理積&であることに注意．乗算*ではない．）
    s = lsb.bit_length()-1  # 「n-1 = (2^s)*d」のsとdを求める．2^s = LSBとする．
    d = m // lsb    # LSB以上のビット部分をdとする．そうすることで，n-1 = (2^s)*dを満たす．

    test_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37] # 与えられる数が2^64未満である場合，aとして以下の配列の値のみを試せば十分．

    #テスト内容 -> A) a^d ≡ 1(mod n) または B) a^((2^r)*d) ≡ -1(mod n)が成り立てば「nは素数である」と判定する．
    for a in test_numbers:
        if a == n: # 任意の自然数kに対してa^k ≡ 0 (mod n)なので無視．
            continue
        x = pow(a,d,n)  # x ≡ a^d(mod n)で初期化．
        r = 0
        if x == 1:  # a^k ≡ 1 (mod n)なので無視．
            continue
        while x != m:   # r = 0からsまで順にx ≡ a^(2^rd) ≡ -1(mod n)を検証．whileループで2の乗算を繰り返す．
            x = pow(x,2,n)
            r += 1
            if x == 1 or r == s:    # x ≡ 1(mod n) -> x^2 ≡ 1(mod n)で-1になり得ないので合成数．
                return 0
    return 1    # すべてのテストを通過したら「nは素数である」と判定して終了．

#約数の探索（素因数分解）を行う．
#「ブレントの循環検出法」を使用．
def find_prime_factor(n):
    if n%2 == 0:     # 偶数なら素因数2を返して終了．
        return 2

    m = int(n**0.125)+1 # GCDの計算をまとめる数、O(n^(1/8))．

    for c in range(1,n):
        f = lambda a: (pow(a,2,n)+c)%n  # 擬似乱数．
        y = 0
        g = q = r = 1
        k = 0
        while g == 1:
            x = y
            while k < 3*r//4:   # k < 3r/4の間はGCDの計算を飛ばす．
                y = f(y)
                k += 1
            while k < r and g == 1:
                ys = y  # バックトラック用の変数．
                for _ in range(min(m, r-k)):    # m個まとめてGCDを計算して途中でGCD>1となったらループを抜ける．
                    y = f(y)
                    q = q*abs(x-y)%n
                g = gcd(q,n)
                k += m
            k = r
            r *= 2  # GCDが1しか見つからなければr = 2rとして繰り返す．
        if g == n:  # GCDがnであればバックトラックして一つずつgcd(|x-y|,n)=1を検証．
            g = 1
            y = ys
            while g == 1:
                y = f(y)
                g = gcd(abs(x-y),n)
        if g == n:  # gcd(|x-y|,n)=nであればcの値を変えてもう一度繰り返す．
            continue
        if is_prime(g): # gcd(|x-y|,n)が素数であればgcd(|x-y|,n)を返して終了．
            return g
        elif is_prime(n//g):    # n/gcd(|x-y|,n)もまたnの約数なので同様に素数であればn/gcd(|x-y|,n)を返して終了．
            return n//g
        else:   # gcd(|x-y|,n), n/gcd(|x-y|,n)が素数でなければgcd(|x-y|,n)に対して再帰的に約数を探索．
            return find_prime_factor(g)


def factorize(n):
    res = []
    p = find_prime_factor(n)    #素因数p,qを探索する．
    q = n // p
    res.append(p)
    res.append(q)
    res = sorted(res) #素因数を昇順に並び替える．
    return res

def main():
    with open('C:/Users/skait/Desktop/graduated_subject/IS/Ns.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        data = ast.literal_eval(content)
        key = 66112300334
        Ns = data[key] #素因数分解すべき合成数Nの集合
        for count, composite_num in enumerate(Ns[:50]):
            factors = factorize(composite_num)
            print(f"{count+1}．「{composite_num}」を素因数分解すると「{factors[0]} * {factors[1]}」です.")

        end = time.time() - start
        print("*---------------------------------*")
        print(f"{count+1}個の計算に{math.floor(end)}秒かかりました．")

if __name__ == "__main__":
    main()