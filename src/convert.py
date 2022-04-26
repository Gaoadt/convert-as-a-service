import tensorflow_hub as tfhub
import tensorflow as tf
import tensorflow_text

# We need to use tensorflow v1 with modern python,
# that is the most straightforward workaround
tf = tf.compat.v1


class ConvertService:
    def __init__(self):
        MODEL_PATH = "data/convert"
        self.sess = tf.InteractiveSession(graph=tf.Graph())
        module = tfhub.Module(MODEL_PATH)

        self.text_placeholder = tf.placeholder(dtype=tf.string, shape=[None])
        self.extra_text_placeholder = tf.placeholder(dtype=tf.string, shape=[None])

        # The encode_context signature now also takes the extra context.
        self.context_encoding_tensor = module(
            {"context": self.text_placeholder, "extra_context": self.extra_text_placeholder}, signature="encode_context"
        )

        self.response_text_placeholder = tf.placeholder(dtype=tf.string, shape=[None])

        self.response_encoding_tensor = module(self.response_text_placeholder, signature="encode_response")
        self.sess.run(tf.tables_initializer())
        self.sess.run(tf.global_variables_initializer())

    def encode_context(self, dialogue_history):
        """Encode the dialogue context to the response ranking vector space.

        Args:
            dialogue_history: a list of strings, the dialogue history, in
                chronological order.
        """

        # The context is the most recent message in the history.
        context = dialogue_history[-1]

        extra_context = list(dialogue_history[:-1])
        extra_context.reverse()
        extra_context_feature = " ".join(extra_context)

        return self.sess.run(
            self.context_encoding_tensor,
            feed_dict={self.text_placeholder: [context], self.extra_text_placeholder: [extra_context_feature]},
        )[0]

    def encode_responses(self, texts):
        return self.sess.run(self.response_encoding_tensor, feed_dict={self.response_text_placeholder: texts})

