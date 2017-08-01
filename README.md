Flask-Ask を使った Alexa Skill のデモ

https://developer.amazon.com/ja/blogs/post/tx14r0iyygh3skt/flask-ask-a-new-python-framework-for-rapid-alexa-skills-kit-development

ngrok を使って
  python memory_game.py
  ./ngrok http 5000

で起動。ngrok の画面に表示された URL を開発者画面の Alexa Skill End
Point に設定する。

Intent と会話モデルは、

```
{
    "intents": [{
        "intent": "YesIntent"
    }, {
        "intent": "AnswerIntent",
        "slots": [{
            "name": "first",
            "type": "AMAZON.NUMBER"
        }, {
            "name": "second",
            "type": "AMAZON.NUMBER"
        }, {
            "name": "third",
            "type": "AMAZON.NUMBER"
        }]
    }]
}
```


```
YesIntent yes
YesIntent sure

AnswerIntent {first} {second} {third}
AnswerIntent {first} {second} and {third}
```
