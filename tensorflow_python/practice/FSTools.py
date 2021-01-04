from cv2 import cv2 as cv
import hashlib
from Crypto.Cipher import AES
import base64
import time
import traceback
# 几个转二进制的函数
# str_2_binstr  将ascii编码表所涵盖的字符转为 位宽位8的 二进制字符串
# number_2_binary_by_bit_width 将数字转为指定位宽的二进制字符串


# str不是16的倍数那就补足为16的倍数
def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)  # 返回bytes


# 加密方法
def encrypt_data(key, message):
    text = base64.b64encode(message.encode('utf-8')).decode('ascii')
    # 初始化加密器
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    # 先进行aes加密
    encrypt_aes = aes.encrypt(add_to_16(text))
    # 用base64转成字符串形式
    encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 执行加密并转码返回bytes
    return encrypted_text


# 解密方法
def decrypt_data(key, encrypted_data):
    # 初始化加密器
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    # 优先逆向解密base64成bytes
    base64_decrypted = base64.decodebytes(encrypted_data.encode(encoding='utf-8'))
    # bytes解密
    decrypted_text = str(aes.decrypt(base64_decrypted), encoding='utf-8') # 执行解密密并转码返回str
    decrypted_text = base64.b64decode(decrypted_text.encode('utf-8')).decode('utf-8')
    return decrypted_text


# 拆分文件
def split_file(origin_src, left_file_src, length_lsb_at_byte, flag):
    with open(origin_src, 'rb') as reader:
        f2 = reader.read()
        lsbstr = ''

        # 将文件进行拆分
        if not flag:
            for i in range(length_lsb_at_byte):
                single_byte = str(hex(f2[i]))[2:]
                single_byte = single_byte if len(single_byte) == 2 else '0' + single_byte
                lsbstr += single_byte
            with open(left_file_src, 'wb') as outfb:
                outfb.write(f2[length_lsb_at_byte:])
            print("需要将文件进行拆分")
        # 不拆分文件
        else:
            print("不需要将文件进行拆分")
            for i in range(len(f2)):
                single_byte = str(hex(f2[i]))[2:]
                single_byte = single_byte if len(single_byte) == 2 else '0' + single_byte
                lsbstr += single_byte

        return lsbstr


# 合并文件
def merge_file(lsbstr, left_src, merge_src, flag):
    lsbbin = bytes()
    for i in range(0, len(lsbstr) - 1, 2):
        lsbbin += bytes.fromhex(lsbstr[i:i + 2])

    if flag:
        with open(merge_src, 'wb') as outfb:
            outfb.write(lsbbin)
    else:
        with open(left_src, 'rb') as pdff:
            left_pdf = pdff.read()
        with open(merge_src, 'ab') as outfb:
            outfb.write(lsbbin)
            outfb.write(left_pdf)


# 文件嵌入：开始嵌入位置选择函数
def get_position_by_secret(secret):
    hash_str = hashlib.md5(secret.encode("utf-8")).hexdigest()
    position_hex = hash_str[5] + hash_str[10] + hash_str[15]
    position = int(position_hex, 16)
    return position if position % 2 == 0 else position -1


# 文件嵌入：获取长度参数
def get_length_file(src):
    with open(src, 'rb') as cover_reader:
        length = len(cover_reader.read())
        return length


# 字符转二进制字符串
def char_2_binary(char):
    # 去掉 bin() 返回的二进制字符串中的 '0b'，并在左边补足 '0' 直到字符串长度为 16
    binary = bin(ord(char))
    binary_char = '0' * (8 - len(binary) + 2) + binary.replace('0b', '')
    return binary_char


# 数字转指定位宽的二进制字符串
def number_2_binary_by_bit_width(number, bit_width):
    binary = bin(number)
    binary_char = '0' * (bit_width - len(binary) + 2) + binary.replace('0b', '')
    return binary_char


# 字符串转二进制字符串
def str_2_binstr(string):
    binary_string = ''.join(map(char_2_binary, string))
    return binary_string


def hexchar_2_binstr(hexchar):
    binstr = bin(int(hexchar, 16))
    result = '0' * (4 - len(binstr) + 2) + binstr.replace("0b", '')
    return result


def hexstr_2_binstr(string):
    return ''.join(map(hexchar_2_binstr, string))


def binstr_2_hexstr(binary):
    list_char = []
    if len(binary) % 4 != 0:
        raise Exception('二进制转十六进制字符串时，二进制字符串不是4的整数倍，出错！')
    while True:
        first_char = binary[0:4]
        binary = binary[4:]
        number = str(hex(int(first_char, 2)))[2:]
        list_char.append(number)
        if len(binary) == 0:
            break
    ret_str = ''.join(list_char)
    return ret_str


# 获取图像像素通道最后一位信息
def get_last_bit(image):
    binary_str = ''
    height, width, cha = image.shape
    for h in range(height):
        for w in range(width):
            for c in range(cha):
                value = image[h, w, c] % 2
                if value == 1:
                    binary_str += '1'
                else:
                    binary_str += '0'
    return binary_str


# 获取加密后文件名二进制的长度
def get_length_filename_at_bit(key, filename):
    filename_binstr = str_2_binstr(encrypt_data(key, filename))
    return len(filename_binstr)


# 获取载体文件中能嵌入的lsb的长度
def get_lsb_length_at_byte_at_cover(key, length_filename, width, height, position):
    return int((width * height * 3 - 300 - position - length_filename)/8)


# 将二进制字符串转为utf8字符串
def binstr_2_str(binary):
    list_char = []
    if len(binary) % 8 != 0:
        raise Exception('提取出错')
    while True:
        first_char = binary[0:8]
        binary = binary[8:]
        number = int(first_char, 2)
        list_char.append(chr(number))
        if len(binary) == 0:
            break
    ret_str = ''.join(list_char)
    return ret_str


def calc_real_position(counter, height, width, cha):
    _height = int(counter / (width * cha))
    _width = int((counter - _height * width * cha) / cha)
    _cha = int((counter - (_height * width * cha) - (_width * cha)) % cha)
    return _height, _width, _cha


# 获取秘密文件可嵌入lsb的字节长度 作废
def get_embed_max_byte_at_secret_file(secret_file_src, key, length_lsb_at_cover_at_byte, length_sr):
    with open(secret_file_src, 'rb') as reader:
        f2 = reader.read()
        length_secret_file = length_sr
        # 先将秘密文件全部加密，判断加密后的字节数是否大于LSB载体可容纳的字节数，
        # 如果大于则需要遍历计算最接近载体可容纳LSB的那个数
        # 如果不大于，则LSB可完全容纳
        lsbstr = ''
        for i in range(length_secret_file):
            single_byte = str(hex(f2[i]))[2:]
            single_byte = single_byte if len(single_byte) == 2 else '0' + single_byte
            lsbstr += single_byte
        # 秘密文件所有数据加密后的长度
        length_encrypted_secret_file_all_data = len(encrypt_data(key, lsbstr))
        if length_lsb_at_cover_at_byte > length_encrypted_secret_file_all_data:
            return length_encrypted_secret_file_all_data
        else:
            previous_len = 0
            current_len = 0
            while True:
                counter = 1
                current_len = len(encrypt_data(key, f2[0:counter]))
                if (current_len > length_lsb_at_cover_at_byte) and (previous_len <= length_lsb_at_cover_at_byte):
                    return previous_len
                else:
                    previous_len = current_len
                    counter += 1


# 数字保留两位小数
def gene_2_num_after_round(number):
    return '%.2f' % number


# 通过文件名获得文件的前缀及后缀
def get_font_end_by_filename(filename):
    comma_index = filename.rfind('.')
    font_filename = filename[:comma_index]
    end_filename = filename[comma_index:]
    return font_filename, end_filename


# 文件lsb嵌入
def embed_file(key, cover_filename, filename, embed_filename):
    print("最新代码/n/n/n")
    start_time = time.time()
    comma_index = filename.rfind('.')
    font_filename = filename[:comma_index]
    end_filename = filename[comma_index:]
    comma_index_cover = cover_filename.rfind('.')
    font_filename_cover = cover_filename[:comma_index_cover]

    cover_src = "./static/imgs/" + cover_filename
    secret_file_src = './static/files/' + filename
    transition_src = "./static/imgs/" + font_filename_cover + "_transition.png"
    left_file_src = "./static/files/" + font_filename + "_left" + end_filename
    result_src = "./static/imgs/" + font_filename_cover + "_result.png"
    print("载体路径：", cover_src)
    print("秘密文件路径:", secret_file_src)
    print("过渡lsb图像路径：", transition_src)
    print("剩余文件路径：", left_file_src)
    print("载迷图像路径", result_src)

    # 秘密文件是否能够全部放入lsb中
    flag = False

    # 获取开始嵌入位置(位)
    position = get_position_by_secret(key)

    # 载体文件的字节大小(字节)
    length_cover_at_byte = get_length_file(cover_src)
    # 秘密文件的字节大小(字节)
    length_secret_file_at_byte = get_length_file(secret_file_src)

    # 获取图像信息(位)
    cover_image = cv.imread(cover_src)
    height, width, cha = cover_image.shape

    # 获取加密后文件名的二进制长度(位)
    length_filename_at_bit = get_length_filename_at_bit(key, embed_filename)
    # 加密后的文件名
    encrypted_filename = encrypt_data(key, embed_filename)
    length_filename = len(encrypted_filename)

    # 秘密文件可嵌入LSB的最大位长度(位)
    length_secret_lsb_at_byte_at_cover_max = get_lsb_length_at_byte_at_cover(key, length_filename_at_bit, width, height, position)


    print("开始嵌入位置(位)：", position)
    print("载体文件大小(字节)：", length_cover_at_byte)
    print("秘密文件大小(字节)：", length_secret_file_at_byte)
    print("文件名长度:", length_filename)
    print("载体中lsb数据段可嵌入的最大长度(字节)：", length_secret_lsb_at_byte_at_cover_max)
    print("载体文件高，宽：", height, width)
    simple_calculation = time.time()
    print("简单计算时间：", (simple_calculation-start_time))

    # 秘密文件嵌入到结构中的字节大小
    if length_secret_lsb_at_byte_at_cover_max >= length_secret_file_at_byte:
        print("lsb中可以存放整个秘密文件")
        flag = True
        length_secret_lsb_at_byte_at_cover = length_secret_file_at_byte
    else:
        flag = False
        print("lsb中不足以存放整个秘密文件")
        print("剩余", length_secret_file_at_byte - length_secret_lsb_at_byte_at_cover_max, "字节数据需要存放到载体文件尾部")
        length_secret_lsb_at_byte_at_cover = length_secret_lsb_at_byte_at_cover_max

    print("嵌入lsb区域文件长度计算时间：", (time.time()-simple_calculation)/1000)

    print("载体中lsb数据段可嵌入的长度(字节)：", length_secret_lsb_at_byte_at_cover)
    print("载体中lsb数据段可嵌入的长度(位)：", length_secret_lsb_at_byte_at_cover * 8)
    print("载体中lsb标识段和数据段共有长度(位)：", length_secret_lsb_at_byte_at_cover * 8 + 300 + length_filename * 8)

    string_2_binary_string_start_time = time.time()
    # 关键字首字符二进制字符串 | 载体文件长度二进制字符串 | 秘密文件长度二进制字符串 | lsb嵌入长度二进制字符串 | 文件名长度二进制字符串 | 文件名二进制字符串 | 文件名字符串 | lsb数据二进制字符串
    bin_first_key = str_2_binstr(encrypt_data(key, key[0]))
    bin_length_cover = number_2_binary_by_bit_width(length_cover_at_byte, 25)
    bin_length_secret_file = number_2_binary_by_bit_width(length_secret_file_at_byte, 25)
    bin_length_secret_lsb = number_2_binary_by_bit_width(length_secret_lsb_at_byte_at_cover, 25)
    bin_length_filename = number_2_binary_by_bit_width(length_filename, 25)
    bin_filename = str_2_binstr(encrypted_filename)
    bin_secret_lsb = hexstr_2_binstr(split_file(secret_file_src, left_file_src, length_secret_lsb_at_byte_at_cover, flag))
    string_2_binary_string_end_time = time.time()
    print("字符转二进制字符串计算时间:", (string_2_binary_string_end_time-string_2_binary_string_start_time))
    no_start_time = time.time()
    print("及时间开始")

    print("bin_first_key(关键字首字符二进制字符串):", bin_first_key)
    # print("bin_length_cover(载体文件长度二进制字符串):", bin_length_cover)
    # print("bin_length_secret_file(秘密文件长度二进制字符串）:", bin_length_secret_file)
    # print("bin_length_secret_lsb(lsb嵌入长度二进制字符串):", bin_length_secret_lsb)
    # print("bin_length_filename(文件名长度二进制字符串):", bin_length_filename)
    # print("bin_filename(文件名二进制字符串):", bin_filename)
    # print("嵌入到lsb中的数据：", bin_secret_lsb[0:1024])

    bin_total = bin_first_key + bin_length_cover + bin_length_secret_file + bin_length_secret_lsb + bin_length_filename + bin_filename + bin_secret_lsb
    result = bin_total
    length_bin_f = len(result)
    print("bin_secret_lsbc长度：", length_bin_f)
    print("bin的后100位：", result[length_bin_f-100:])

    no_end_time = time.time()
    print("及时间：", (no_end_time-no_start_time))

    read_start_time = time.time()
    pixel_list = []
    for h in range(height):
        for w in range(width):
            for c in range(cha):
                pixel_list.append(cover_image[h, w, c])
    read_end_time = time.time()
    print("读取图像加入列表时间：", (read_end_time - read_start_time))

    # 开始嵌入
    print("开始嵌入")
    embed_start_time = time.time()
    counter = 0

    while True:
        if counter >= position: # 判断是否可以开始嵌入
            if len(bin_total) == 0:
                break
            _h, _w, _c = calc_real_position(counter, height, width, cha)
            first_char = bin_total[0]
            bin_total = bin_total[1:]
            first_int = int(first_char)
            value = pixel_list[counter] % 2
            if first_int == 1 and value == 0:
                cover_image[_h, _w, _c] = cover_image[_h, _w, _c] + 1
            elif first_int == 0 and value == 1:
                cover_image[_h, _w, _c] = cover_image[_h, _w, _c] - 1
        counter += 1
            # print(cover_image[h, w, c])

    # 保存图像
    cv.imwrite(transition_src, cover_image)
    embed_end_time = time.time()
    print("嵌入时间：", (embed_end_time-embed_start_time))

    append_start_time = time.time()
    print("追加开始")
    if not flag:
        with open(left_file_src, 'rb') as left_secret_file_reader:
            with open(transition_src, 'rb') as cover_reader:
                with open(result_src, 'ab') as result_write:
                    left_file_data = left_secret_file_reader.read()
                    lsb_img_data = cover_reader.read()
                    result_write.write(lsb_img_data)
                    result_write.write(left_file_data)
    else:
        with open(transition_src, 'rb') as cover_reader:
            with open(result_src, 'ab') as result_write:
                lsb_img_data = cover_reader.read()
                result_write.write(lsb_img_data)
    append_end_time = time.time()
    print("计算追加及追加时间：", (append_end_time-append_start_time))
    end_time = time.time()
    result = {"success": 1, "time": gene_2_num_after_round(end_time - start_time), "info": "隐写成功", "flag": flag}
    return result


def extract_file(stego_name, key):
    start_time = time.time()
    # 默认有追加的二进制文件
    flag = False
    try:
        font_name, end_name = get_font_end_by_filename(stego_name)
        lsb_img_src = "./static/imgs/" + stego_name

        position = get_position_by_secret(key)
        print("开始嵌入位置：", position)
        # 1.校验首字符
        first_key = key[0]
        total_binstr = get_last_bit(cv.imread(lsb_img_src))
        binstr = total_binstr[position:]


        # 关键字首字符二进制字符串 | 载体文件长度二进制字符串 | 秘密文件长度二进制字符串 | lsb嵌入长度二进制字符串 | 文件名长度二进制字符串 | 文件名二进制字符串 | lsb数据二进制字符串
        bin_first_key = binstr[:200]

        # 关键字首字符 | 载体文件长度 | 秘密文件长度 | lsb嵌入长度 | 文件名长度 | 文件名 | 文件名字符串 | lsb数据
        first_key_by_extract = decrypt_data(key, binstr_2_str(bin_first_key))
        if first_key == first_key_by_extract:
            bin_length_cover = binstr[200:225]
            bin_length_secret_file = binstr[225:250]
            bin_length_secret_lsb = binstr[250:275]
            bin_length_filename = binstr[275:300]
            length_secret_lsb = int(bin_length_secret_lsb, 2) * 8
            length_filename = int(bin_length_filename, 2) * 8
            bin_filename = binstr[300:300 + length_filename]
            bin_secret_lsb = binstr[300 + length_filename:300 + length_filename + length_secret_lsb]
            hex_secret_lsb = binstr_2_hexstr(bin_secret_lsb)
            length_cover = int(bin_length_cover, 2)
            length_secret_file = int(bin_length_secret_file, 2)
            print("秘钥首字符解码：", first_key_by_extract)
            print("载体文件长度：", length_cover)
            print("秘密文件长度：", length_secret_file)
            print("lsb嵌入长度", length_secret_lsb)
            print("文件名长度", length_filename)
            print("bin_secret_lsbc长度：", len(bin_secret_lsb))
            filename = decrypt_data(key, binstr_2_str(bin_filename))
            print("文件名", filename)
            this_a_scr, secret_file_suffix = get_font_end_by_filename(filename)
            extract_left_src = "./static/files/" + font_name + "_extract_left" + secret_file_suffix
            extract_result_file_src = "./static/files/" + font_name + "_extract_result" + secret_file_suffix

            print("载密图像路径：", lsb_img_src)
            print("结构嵌入文件路径：", extract_left_src)
            print("提取结果文件路径：", extract_result_file_src)


            left_size = int(length_secret_file-length_secret_lsb / 8)
            print("剩余大小：", left_size)
            with open(lsb_img_src, 'rb') as cover_reader:
                with open(extract_left_src, 'wb') as left_file_write:
                    lsb_img_data = cover_reader.read()
                    # 如果秘密文件长度 > lsb长度，那么需要left_file文件
                    if length_secret_file > length_secret_lsb / 8:
                        print("需要left_file路径")
                        left_file_write.write(lsb_img_data[len(lsb_img_data)-left_size:])
                        flag = False
                    else:
                        flag = True
                        print("不需要left_file路径，没有剩余文件")

            merge_file(hex_secret_lsb, extract_left_src, extract_result_file_src, flag)
            end_time = time.time()
            result = {"success": 1, "time": gene_2_num_after_round(end_time - start_time), "info": "提取成功", "flag": flag, "filename": filename}
            return result
        else:
            end_time = time.time()
            result = {"success": 0, "time": gene_2_num_after_round(end_time - start_time), "info": "秘钥错误或非载密体", "flag": flag}
            return result
    except Exception as e:
        end_time = time.time()
        print(e)
        traceback.print_exc()
        result = {"success": 0, "time": gene_2_num_after_round(end_time - start_time), "info": "秘钥错误或非载密体", "flag": flag}
        return result


if __name__ == "__main__":
    # 嵌入过程的参数
    cover_src = "timg.jpg"
    # 文件名&文件路径
    filename = "001.pdf"
    embed_name = "his.pdf"
    # 秘钥(注意：仅为英文字符)
    keys = "nb"
    # 文件剩余部分嵌入路径

    # 提取参数
    stego_name = "timg_result.png"

    # print("-------------------嵌入过程--------------------")
    # info = embed_file(keys, cover_src, filename, embed_name)
    # print(info)

    print("-------------------提取过程--------------------")
    print(extract_file(stego_name, keys))
