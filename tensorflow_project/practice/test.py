import tensorflow as tf
tf.compat.v1.disable_eager_execution()
def tensorflow_demo():
    # 自定义图
    mine=tf.Graph()
    # 在自己定义的图中定义数据和操作
    with mine.as_default():

        a=tf.constant(2)
        print("a的图属性：\n",a.graph)
        b=tf.constant(3)
        print("b的图属性：\n", b.graph)
        c=tf.add(a,b)
    # 开启mine的会话
    with tf.compat.v1.Session(graph=mine) as sess:
        # tensorflow实现加法运算的结果
        result=sess.run(c)
        print(c)
    #    将图写入本地，生成events文件
        tf.compat.v1.summary.FileWriter('D:\suibian\python练习项目\summary',graph=sess.graph)
    return None

def one():
    a = tf.compat.v1.placeholder(tf.float32)
    b = tf.compat.v1.placeholder(tf.float32)
    sum = tf.add(a,b)
    with tf.compat.v1.Session() as sess:
        print("占位符结果：\n",sess.run(sum,feed_dict={a:3.0,b:2.0}))

# 创建张量
def createZL():
    # zero = tf.zeros(shape=[3,4],dtype=tf.float32,name=None)
    # zero = tf.ones(shape=[3, 4], dtype=tf.float32, name=None)
    zero = tf.compat.v1.random_normal(shape=[2,5],mean=1.75,stddev=0.12,dtype=tf.float32)
    with tf.compat.v1.Session() as sess:
        print(sess.run(zero))

# 张量类型的修改
def upZl():
    a = tf.constant(5,dtype=tf.int16)
    print("转换之前的类型：\n",a)
    b = tf.compat.v1.cast(a,dtype=tf.float32)
    print("转换之后的类型：\n",b)

# 张量变换形状
def upXZ():
    # 没有完全固定下来的静态形状
    a = tf.compat.v1.placeholder(dtype=tf.float32,shape=[None,None])
    b = tf.compat.v1.placeholder(dtype=tf.float32, shape=[None, 3])
    print("没有完全固定下来的静态形状 a：\n",a)
    print("没有完全固定下来的静态形状 b：\n", b)
    a.set_shape([3,4])
    b.set_shape([5, 3])
    print("固定下来的静态形状 a：\n", a)
    print("固定下来的静态形状 b：\n", b)

def dongtai():
    a = tf.compat.v1.placeholder(dtype=tf.float32, shape=[None, None])
    b = tf.reshape(a,shape=[2,3,2])
    print("变之前：\n",a)
    print("变之后：\n", b)

def createBL():
    a = tf.Variable(initial_value=50)
    b = tf.Variable(initial_value=40)
    c = tf.add(a,b)
    print("a：\n",a)
    print("b：\n", b)
    print("c：\n", c)
    # 初始化变量
    init = tf.compat.v1.global_variables_initializer()
    # 开启会话
    with tf.compat.v1.Session() as sess:
        # 运行初始化
        sess.run(init)
        a_value,b_value,c_value = sess.run([a,b,c])
        print("a_value：\n", a_value)
        print("b_value：\n", b_value)
        print("c_value：\n", c_value)
if __name__ == '__main__':
    createBL()
