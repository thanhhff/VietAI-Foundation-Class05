import matplotlib.pyplot as plt
from ex1_linear_known_model import *
from utils import generate_data, visualize_data, normalize_feature

np.random.seed(2018)
tf.set_random_seed(2018)


def draw_model(a, b):
    # Draw line y = ax + b
    x = np.arange(-3, 3, 0.2)
    y = a * x + b
    plt.plot(x, y)


def main():
    # Step 1: Generate and visualize training data
    X_train, Y_train, X_test, Y_test = generate_data(3, 0, train_set_ratio=0.9)
    visualize_data(X_train, Y_train)
    n_samples = len(X_train)

    # Step 1b: Normalize Xs and re-visualize training data
    X_train, mean_train, std_train = normalize_feature(X_train, mode='train')
    X_test = normalize_feature(X_test, mode='test',
                               mean=mean_train, std=std_train)
    visualize_data(X_train, Y_train, viz_trainining=True)
    print('mean_train=', mean_train, ', std_train=', std_train)

    # Step 2: Initialize Placeholders for input data
    X = tf.placeholder(shape=[None], dtype=tf.float32, name='X')
    Y = tf.placeholder(shape=[None], dtype=tf.float32, name='Y')

    # Step 3: Build up your model graph
    a_sym, b_sym, = define_parameters()
    cost = define_cost_func(X, Y, a_sym, b_sym, n_samples)

    cost_summary = tf.summary.scalar(name='cost', tensor=cost)

    # Step 4: Create optimizer op and initializer op
    learning_rate = 0.1
    optimizer, initializer = define_optimizer(learning_rate, cost)

    with tf.Session() as sess:
        writer = tf.summary.FileWriter('log', graph=sess.graph)
        sess.run(initializer)
        for i in range(400):
            _, cost_train, cost_sum_val = sess.run([optimizer, cost, cost_summary], feed_dict={X: X_train, Y: Y_train})

            writer.add_summary(cost_sum_val, global_step=i)
            a, b = sess.run([a_sym, b_sym])
            cost_test = sess.run(cost, feed_dict={X: X_test, Y: Y_test})
            print('a_scale=', a, 'b_scale=', b)
            print('a=', a/std_train, 'b=', b - a*mean_train/std_train)
            print('Training Cost =', cost_train, "\tTesting Cost =", cost_test)
            plt.plot(X_train, Y_train, 'bo')
            draw_model(a, b)
            plt.pause(0.1)

    print('Optimized variable: a = ', a)
    print('Optimized variable: b = ', b)


if __name__ == '__main__':
    main()
