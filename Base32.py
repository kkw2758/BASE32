#BASE32 Encoding
#a += b => a = a + b OR a = b + a


def make_encode_book():#인코딩할때 참고할 딕셔너리를 만들어 주는 함수
	encode_book = {}
	
	for x in range(26):
		encode_book[x] = chr(x+65)
		
	for x in range(6):
		encode_book[26+x] = str(x+2) #딕셔너리 key error 조심 정수3과 문자 '3'은 다르다.
	
	return encode_book
	
def BIN_to_DEC(binary):#2진수를 10진수로 변환하여 리턴해주는 함수
	sum = 0
	for x in range(len(binary)):
		sum += int(binary[x])*(2**(len(binary)-x-1))
	return sum
	
def Encoding(plaintext):#인코딩의 반대과정 인코딩 => 각문자를 8비트의 크기의 비트열로 바꾼다. -> 인코딩할 비트열의 길이를 40의 배수로 맞춰준다. -> 앞에서부터 5비트씩 끊어서 encode_book을 통해 치환한다. -> '='으로 패딩

	encode_book = make_encode_book()	#인코딩할때 참고할 딕셔너리를 만든다.
	binary_result = ''					#입력된 문자를 2진수로 바꾼값을 담을 빈문자열
	
	for x in plaintext:					#2진수 비트열 만들기
		binary = bin(ord(x))		
		original_binary = binary[2:]	#bin()함수를 사용하면 결과로 '0b'가 붙은 값을 돌려주는데 '0b'에는 볼일이 없으므로 슬라이싱을 사용해서 제거
		
		if len(original_binary)%8 != 0:	#base32 인코딩과정에서 한 문자를 8비트로 만들어준다.
			original_binary = '0'*(8 - len(original_binary)) + original_binary # +=에 유의
			binary_result += original_binary 
		else:
			binary_result += original_binary
	
	if len(binary_result)%40 != 0:	#비트열의 길이를 40의 배수가 되도록한다.
		binary_result += '0'*(40 - len(binary_result)%40)
		
	ciphered = ''	#인코딩된 결과를 받을 빈문자열
	
	for x in range(len(binary_result)//5):#비트열의 길이가 40의 배수로 맞춰줬기때문에 5로 나누어 떨어지고 비트열의 길이를 5로 나눈 값이 인코딩된 문자열의 길이이다.
		dict_key = BIN_to_DEC(binary_result[5*x:5*(x+1)])#비트열의 앞부터 5개씩 잘라서 10진수로 바꿔준다.
		ciphered += str(encode_book[dict_key])			 #제일 위에서 선언한 encode_book을 참고하여 치환한다.
	
	if len(plaintext)%5 == 1:	#인코딩과정에서 비트열의 길이를 40의 배수로한다고 비트열 뒤에 0을 추가하고 치환하는 작업이있었는데 이 0은 의미없는 값이므로 문자열의 길이에따라 '='을 붙여준다.
		ciphered = ciphered[:-6] + '='*6
	elif len(plaintext)%5 == 2:
		ciphered = ciphered[:-4] + '='*4
	elif len(plaintext)%5 == 3:
		ciphered = ciphered[:-3] + '='*3
	elif len(plaintext)%5 == 4:
		ciphered = ciphered[:-1] + '='*1
	
	return ciphered


'''인코딩 과정
===============================================================================================================================================================================
'''
def make_decode_book():				#디코딩 할때 참고할 딕셔너리를 만들어주는 함수
	encode_book = make_encode_book() 
	decode_book = {}
	for x in encode_book:
		decode_book[encode_book[x]] = x
	return decode_book				#인코딩 과정에서 사용한 make_encode_book의 key와 value 값의 자리를 바꾼 딕셔너리 
	
def Decoding(encoded):				#'='으로 패딩된값 무시 -> 인코딩된 결과를 decode_book을 참고하여 각문자를 5비트로 만든다. ->앞에서부터 8비트씩 끊어서 문자에 대응시킨다.

	decode_book = make_decode_book()
	binary_result =''
	
	for x in encoded:
		if x != '=':					#base32에서 디코딩할때 '='은 의미없는값이므로 무시한다.
			binary = bin(decode_book[x])
			binary = binary[2:]
			if len(binary) != 5:
				original_binary = '0'*(5-len(binary)) + binary
				binary_result += original_binary
			else:
				binary_result += binary
				
	deciphered = ''
	
	for y in range(len(binary_result)//8):
		result = chr(BIN_to_DEC(binary_result[0 + 8*y : 8 + 8*y]))
		deciphered += result
	return deciphered

	
def main():
	Plaintext = input("인코딩할 문자열을 입력하시오 :")
	encoded = Encoding(Plaintext)
	print('Encoding ->',encoded)
	decoded = Decoding(encoded)
	print('Decoding ->',decoded)
	
if __name__ == "__main__":
	main()