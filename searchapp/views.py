from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json, os
from . import file_reader
from gensim.models import Word2Vec
import nltk
import gensim
from .models import File
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import sqlite3

model = None


def train_db(request):
    global model
    path = request.GET['path']
    corpus = connectSQL(path, 'text', 'files')

    tok_corp = [nltk.word_tokenize(str(sent).lower()) for sent in corpus]
    print("Training model")
    if len(tok_corp) == 0:
        return JsonResponse({'result': 'No new training data found'})
    if model is None:
        model = gensim.models.Word2Vec(tok_corp, min_count=1, size=32)
        model.save('models\\final_model.model')
    else:
        model.train(tok_corp)
        model.save()
    print("Done")
    return JsonResponse({'result': 'Successful'})


def connectSQL(database, fields, table):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute("SELECT {} FROM {}".format(fields, table))
    results = cursor.fetchall()
    count = 0
    for result in results:
        try:
            file = File(name=result['id'], full_text=result['text'])
            file.save()
        except:
            print("\rThere was some error processing file id: {}".format(result['id']))
        count += 1
        print("\rFiles analyzed: {}".format(count), end='')
    print("\nDone")
    return results


def train(request):
    global model
    # path = "C:\Users\anuj\Desktop\text"
    path = request.GET['path']
    print("Training from path: {}".format(path))
    path = '\\'.join(path.split('\\'))
    file_count = 0
    corpus = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            file_count += 1
            path = str(os.path.join(dirpath, filename))
            files = File.objects.filter(path=path)
            if len(files) > 0:
                print("\rFile at {} already exists in database".format(path))
                continue
            print("\rTotal files analyzed: {} ".format(file_count), end='')
            if filename.endswith('.txt'):
                # try:
                text = file_reader.read_txt(os.path.join(dirpath, filename))
                file_type = '.txt'
                file = File(name=filename.split('.')[0], path=path, full_text=text, type=file_type)
                file.save()
                corpus.append(text)
                # except:
                #     print("Some error processing {}".format(os.path.join(dirpath, filename)))
            elif filename.endswith('.docx'):
                try:
                    text = file_reader.read_docx(os.path.join(dirpath, filename))
                    file_type = '.docx'
                    file = File(name=filename.split('.')[0], path=path, full_text=text, type=file_type)
                    file.save()
                    corpus.append(text)
                except:
                    print("Some error processing {}".format(os.path.join(dirpath, filename)))
            elif filename.endswith('.pptx'):
                try:
                    text = file_reader.read_pptx(os.path.join(dirpath, filename))
                    file_type = '.pptx'
                    file = File(name=filename.split('.')[0], path=path, full_text=text, type=file_type)
                    file.save()
                    corpus.append(text)
                except:
                    print("Some error processing {}".format(os.path.join(dirpath, filename)))
            elif filename.endswith('.pdf'):
                try:
                    text = file_reader.read_pdf(os.path.join(dirpath, filename))
                    file_type = '.pdf'
                    file = File(name=filename.split('.')[0], path=path, full_text=text, type=file_type)
                    file.save()
                    corpus.append(text)
                except:
                    print("Some error processing {}".format(os.path.join(dirpath, filename)))
    print("\n Data Fetched, Processing")
    tok_corp = [nltk.word_tokenize(str(sent).lower()) for sent in corpus]
    print("Training model")
    if len(tok_corp) == 0:
        return JsonResponse({'result': 'No new training data found'})
    if model is None:
        model = gensim.models.Word2Vec(tok_corp, min_count=1, size=32)
        model.save('models\\final_model.model')
    else:
        model.train(tok_corp)
        model.save()
    print("Done")
    return JsonResponse({'result': 'Successful'})


def search(request):
    global model
    query = request.GET['query']
    method = request.GET['method']
    if method == 'name':
        result = search_with_name(query)
    elif method == 'tag':
        result = search_with_tags(query)
    elif method == 'text':
        result = search_with_text(query)
    elif method == 'similar':
        result = []
        global model
        if model is None:
            try:
                model = Word2Vec.load('models\\final_model.model')
            except FileNotFoundError:
                return JsonResponse({
                    'id': 0,
                    'name': "Not Found",
                    'text': "No model found, Please add a directory containing .txt, .pptx, .docx or .pdf files to "
                            "add them to the database",
                    'path': "Or contact administration for more details",
                    'type': ' Error',
                })
        try:
            similar_words = model.most_similar(query)
            print("Trying similar words:")
            for (word, cos) in similar_words:
                print(word)
                result += (search_with_text(word))
        except KeyError:
            print("Not found in vocab")
        finally:
            print("Done")
    else:
        result = []
    # result = (search_with_name(query))
    # print(result)
    return JsonResponse(result, safe=False)


def get_file_info(request):
    fid = request.GET['id']
    print("Getting file info for id: {}".format(fid))
    file = File.objects.get(id=fid)
    return JsonResponse({
            'id': file.id,
            'name': file.name,
            'text': file.full_text,
            'tags': file.user_tags + file.automatic_tags,
            'path': file.path,
            'type': file.type
    })


@csrf_exempt
def add_tags(request):
    data = json.loads(request.body.decode('utf-8'))
    filepath = data['filepath']
    tags = data['tags']
    file = File.objects.get(path=filepath)
    file.user_tags += "{} ".format(tags)
    file.save()
    print(filepath)
    return JsonResponse("Done Successfully", status=200, safe=False)


def search_with_name(query):
    # File name search
    try:
        print(query)
        files = File.objects.filter(name__icontains=query)
        result = [{
            'id': i.id,
            'name': i.name,
            'text': i.full_text[:400],
            'tags': i.user_tags + i.automatic_tags,
            'path': i.path,
            'type': i.type
        }
            for i in files]
        return result
        # return files
    except File.DoesNotExist:
        return "No file found"


def search_with_tags(query):
    try:
        files = File.objects.filter(Q(user_tags__contains=query) | Q(automatic_tags__contains=query))
        result = [{
            'id': i.id,
            'name': i.name,
            'text': i.full_text[:400],
            'tags': i.user_tags + i.automatic_tags,
            'path': i.path,
            'type': i.type
        }
            for i in files]
        return result
        # return files
    except File.DoesNotExist:
        return "Not found"


def search_with_text(query):
    try:
        files = File.objects.filter(full_text__icontains=query)
        result = [{
            'id': i.id,
            'name': i.name,
            'text': i.full_text[max(i.full_text.lower().find(query.lower()) - 200, 0):
                                min(i.full_text.lower().find(query.lower()) + 200, len(i.full_text))],
            'tags': i.user_tags + i.automatic_tags,
            'path': i.path,
            'type': i.type
        }
            for i in files]
        return result
    except File.DoesNotExist:
        return "Not found"

# TODO: To add SQL support
