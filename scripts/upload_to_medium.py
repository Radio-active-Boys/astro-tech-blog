import os
import frontmatter
import glob
import requests
import time 
from dateutil.parser import parse
from datetime import datetime
from dotenv import load_dotenv

def publish_to_medium(data):
    """
    Publishes data to Medium.

    Args:
        data (dict): A dictionary containing the data to be published.

    Returns:
        bool: True if the article is successfully created, False otherwise.
    """
    token = os.getenv("MEDIUM_TOKEN")
    baseUrl = "https://friendlyuser.github.io"
    canonicalUrl = f"{baseUrl}{data['slug']}"
    # url encode imgSrc
    adjustedImgSrc = data["imgSrc"].replace(" ", "%20").replace("ﾂｷ","·")
    titleImg = f'![title img]({baseUrl}{adjustedImgSrc})'
    adjustedContent = data.content.replace("![markdown](/imgs/", f"![markdown]({baseUrl}/imgs/")
    full_content = f"{titleImg} \n \n {adjustedContent}"
    article = {
        "title": data["title"],
        "contentFormat": "markdown",
        "content": full_content,
        "canonicalUrl": canonicalUrl,
        # "tags": data["tags"],
        "publishStatus": "draft"
    }

    user_info = requests.get(f"https://api.medium.com/v1/me?accessToken={token}")
    user_json_info = user_info.json()

    header = {
        "Authorization": f"Bearer {token}"
    }

    post_request = requests.post(f"https://api.medium.com/v1/users/{user_json_info['data']['id']}/posts", headers = header, data = article)

    if post_request.status_code == requests.codes.created:
      print(post_request)
      return True
    else:
      print("Failed to create article")
      print(f"Code is: "  + str(post_request.status_code))
      return False

def make_articles_for_medium():
    """
    Generates a function comment for the given function body in a markdown code block with the correct language syntax. 
    
    Returns:
        str: The function comment for the given function body.
    """
    basePostFolder = "src/pages"
    postFolders = ["posts/stonks/web", "posts/stonks/ta", "posts", "posts/stonks", "posts/tech", "posts/tech/css", "posts/tech/dapps", "posts/tech/flutter", "posts/tech/java", "posts/tech/js", "posts/tech/net", "posts/tech/python", "posts/tech/scripting", "posts/tech/go", "posts/random", "posts/tech/utils", "posts/tech/2023", "posts/tech/php", "posts/tech/python/introToPython", "posts/tech/rust", "posts/tech/react", 
    "posts/tech/js/ui", "posts/stonks/thoughts", 
    "posts/tech/tex", "posts/tech/python/projects", "posts/tech/vue", "posts/tech/autohotkey", "posts/tech/ai", "posts/tech/cpp", "posts/tech/deno", "posts/tech/kotlin"]
    # read articles from medium_articles
    created_articles = []
    with open ("scripts/medium_articles.txt", "r") as f:
        for line in f.readlines():
            created_articles.append(line.strip())


    posted_articles = 0
    max_posted_articles = 50
    # find all markdown files in the post folders
    for postFolder in postFolders:
        for post in glob.glob(f"{basePostFolder}/{postFolder}/*.md"):
            if posted_articles >= max_posted_articles:
              print("Max articles posted")
              break
            with open(post, encoding="utf-8", errors="replace") as f:
              post_contents = frontmatter.loads(f.read())
            # strip basePostFolder from the path
            adjustedPost = post.replace(basePostFolder, "")
            # convert adjustedPost to linux file path
            adjustedPost = adjustedPost.replace("\\", "/")
            # publish_to_medium(post)
            # make sure frontMatter has a date in the future
            # pubDate > currDate
            try:
              if parse(post_contents["pubDate"]).replace(tzinfo=None) < datetime.now():
                  # print(f"Skipping {adjustedPost} because date is in the past")
                  continue
              else: 
                  pass
            except Exception as e:
              print(e)
              pass
            if adjustedPost not in created_articles:
                print(f"Publishing {adjustedPost}")
                post_contents["slug"] = adjustedPost
                isCreated = publish_to_medium(post_contents)
                if isCreated:
                  created_articles.append(adjustedPost)
                  posted_articles += 1
                else: 
                  time.sleep(5)
                time.sleep(0.5)
    with open ("scripts/medium_articles.txt", "w") as f:
        for article in created_articles:
            f.write(article + "\n")

def make_articles_for_dev():
  pass

def main():
  try:
    load_dotenv()
  except Exception as e:
    raise e
  make_articles_for_medium()

if __name__ == "__main__":
    main()
