# tensorflow==1.14.0
# tensorflow_text==0.1.0
# tensorflow-hub==0.7.0
# wget http://files.deeppavlov.ai/alexaprize_data/convert_reddit_v2.8.tar.gz
# tar xzfv .....
# MODEL_PATH=........../convert_data/convert

import os

import tensorflow_hub as tfhub
import tensorflow as tf
import tensorflow_text

tf = tf.compat.v1

from tqdm.notebook import trange

tensorflow_text.__name__

# MODEL_PATH = os.getenv("MODEL_PATH")
MODEL_PATH = "convert"

sess = tf.InteractiveSession(graph=tf.Graph())

module = tfhub.Module(MODEL_PATH)

text_placeholder = tf.placeholder(dtype=tf.string, shape=[None])
extra_text_placeholder = tf.placeholder(dtype=tf.string, shape=[None])

# The encode_context signature now also takes the extra context.
context_encoding_tensor = module(
    {"context": text_placeholder, "extra_context": extra_text_placeholder}, signature="encode_context"
)

responce_text_placeholder = tf.placeholder(dtype=tf.string, shape=[None])

response_encoding_tensor = module(responce_text_placeholder, signature="encode_response")

sess.run(tf.tables_initializer())
sess.run(tf.global_variables_initializer())


def encode_context(dialogue_history):
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

    return sess.run(
        context_encoding_tensor,
        feed_dict={text_placeholder: [context], extra_text_placeholder: [extra_context_feature]},
    )[0]


def encode_dialogues(dialogues):
    histories = [" ".join(u.utterance for u in dialogue[:k][::-1])
                 for dialogue in dialogues
                 for k in range(len(dialogue))]
    utterances = dialogues.utterances

    print(len(histories))
    print(len(utterances))

    parts = []
    step = 1000
    for i in trange(0, len(utterances), step):
        parts.append(sess.run(
            context_encoding_tensor,
            feed_dict={text_placeholder: utterances[i:i + step],
                       extra_text_placeholder: histories[i:i + step]},
        )[0])
    return parts


def encode_responses(texts):
    return sess.run(response_encoding_tensor, feed_dict={responce_text_placeholder: texts})