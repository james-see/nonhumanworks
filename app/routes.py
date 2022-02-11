from app import app
import redis

r = redis.StrictRedis(decode_responses=True)


def filterprofanity(stringtocheck) -> (bool):
    stringtochecklist = stringtocheck.split()
    print(stringtochecklist)
    templist = []
    with open('profanity.txt') as f:
        for line in f:
            templist.append(line.split('\n')[0].strip("\'"))
    # print(templist)
    for val in templist:
        if val in stringtochecklist:
            print("fouind")
            return False
    return True
    



@app.route('/api/')
@app.route('/index')
def index():
    return "Welcome to Anduril AI Art Generator! Simply pass in the phrase you want to use in the url itself, for example <a href='http://10.10.200.19/api/dogs%20playing%20golf'>http://10.10.200.19/api/dogs playing golf</a>"


@app.route('/api/<id>') 
def landing_page(id):
    safe = filterprofanity(id)
    if safe:
        print(f"What I received was {id}. Adding to queue.")
        r.sadd("prompts", id)
        # runner.do_run(id)
        return f"<!DOCTYPE html><body style='font-family:monospace;'><h4>What was received was the following prompt: {id}</h4><h4>Added to queue. The image will be available at <a href='http://10.10.200.19/static/{id}.png'>http://10.10.200.19/static/{id}.png</a>. Estimated time 5 minutes. The queue is polled every minute and is randomly selected. </h4><h4>See QueueList <a href='http://10.10.200.19/api/queuelist'>here</a></h4><h4>See what is currently being worked on: <a href='http://10.10.200.19/api/current'>http://10.10.200.19/api/current</a></h4></body></html>"
    else:
        return f"<!DOCTYPE html><body style='font-family:monospace;'><h4>You hit the profanity filter. What you typed in is NSFW. Please try again. <a href='http://10.10.200.19/api/'>back to api</a></h4>"


@app.route('/api/queuecount')
def queue_count():
    totalqueue = r.scard("prompts")
    return f"<!DOCTYPE html><body style='font-family:monospace;'><h4>Queue to process: {totalqueue}</h4>"


@app.route('/api/queuelist')
def queue_list():
    listmembers = r.smembers("prompts")
    if len(listmembers) < 1:
        listmembers = ["None"]
    fixedlist = [x + "<br>" for x in listmembers]
    fixedstring = "".join(fixedlist)
    current = r.get("current")
    return f"<!DOCTYPE html><body style='font-family:monospace;'><h4>Queue to process:<br><br> {fixedstring}</h4><h4>Currently working on: <a target='_blank' href='http://10.10.200.19/api/current'>{current}</a></h4></body>"


@app.route('/api/current')
def get_current():
    listmembers = r.smembers("prompts")
    if len(listmembers) < 1:
        listmembers = ["None"]
    fixedlist = [x + "<br>" for x in listmembers]
    fixedstring = "".join(fixedlist)
    currentwork = r.get("current")
    return f"<!DOCTYPE html><body style='font-family:monospace;'><h4>Currently working on: <a href='http://10.10.200.19/static/{currentwork}.png'>{currentwork}</a> (click to peek at the current iteration as it is working)</h4><h4><a target='_blank' href='http://10.10.200.19/api/queuelist'>Queue</a> to process:<br><br> {fixedstring}</h4><h4>View the current <a href='http://10.10.200.19/gallery.php'>gallery</a>.</h4>"