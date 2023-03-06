import js2py

translate_video = js2py.eval_js(open('./weibo/test.js', 'r', encoding='utf-8').read())

translate_video()