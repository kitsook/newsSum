import NewsSource from "../models/NewsSource";
import NewsArticle from "../models/NewsArticle";
import Logger from "./Logger";

export default class NewsSumApi {
  static async getSources(): Promise<NewsSource[]> {
    try {
      // TODO use relative url
      var response = await fetch(process.env.NODE_ENV !== 'production'? "https://news-sum.appspot.com/list" : "/list", {
        "method": "GET",
      });
      if (response.ok) {
        return <NewsSource[]>(await response.json());
      } else {
        Logger.log("Failed to fetch news sources " + response.status + ": " + response.statusText);
      }
    } catch (err: unknown) {
      Logger.log("Failed to fetch news sources: ");
      if (typeof err === "string") {
        Logger.log(err);
      } else if (err instanceof Error) {
        Logger.log(err.message);
      }
    }
    return Promise.reject("Failed to retrieve news sources");
  }

  static async getArticles(path: string): Promise<NewsArticle[]> {
    try {
      // TODO use relative url
      var response = await fetch(process.env.NODE_ENV !== 'production'? "https://news-sum.appspot.com/" + path : "/" + path, {
        "method": "GET",
      })
      if (response.ok) {
        return <NewsArticle[]>(await response.json());
      } else {
        Logger.log("Failed to load content for " + path + " with status " + response.status + ": " + response.statusText);
      }
    } catch (err: unknown) {
      Logger.log("Failed to load content: ");
      if (typeof err === "string") {
        Logger.log(err);
      } else if (err instanceof Error) {
        Logger.log(err.message);
      }
    }

    return Promise.reject("Failed to load content");
  }
}
