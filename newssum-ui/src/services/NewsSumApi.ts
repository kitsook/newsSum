import NewsSource from "../models/NewsSource";
import NewsArticle from "../models/NewsArticle";
import Logger from "./Logger";

export default class NewsSumApi {
  static async getSources(): Promise<NewsSource[]> {
    try {
      // TODO setup url for dev
      const response = await fetch(process.env.NODE_ENV !== 'production'? "https://news-sum.appspot.com/list" : "/list", {
        "method": "GET",
      });
      if (response.ok) {
        const sources: NewsSource[] = <NewsSource[]>(await response.json());
        sources.sort((a, b) => a.desc < b.desc? -1 : 1);
        return sources;
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
    return Promise.reject(new Error("Failed to retrieve news sources"));
  }

  static async getArticles(path: string): Promise<NewsArticle[]> {
    try {
      // TODO setup url for dev
      const response = await fetch(process.env.NODE_ENV !== 'production'? "https://news-sum.appspot.com/" + path : "/" + path, {
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

    return Promise.reject(new Error("Failed to load content"));
  }

  static async getAppProperties(): Promise<Map<string, string>> {
    try {
        // TODO setup url for dev
        const response = await fetch(process.env.NODE_ENV !== 'production'? "https://news-sum.appspot.com/about" : "/about", {
          "method": "GET",
        });
        if (response.ok) {
            return new Map<string, string>(Object.entries(await response.json()));
        } else {
          Logger.log("Failed to fetch app properties " + response.status + ": " + response.statusText);
        }
      } catch (err: unknown) {
        Logger.log("Failed to fetch app properties: ");
        if (typeof err === "string") {
          Logger.log(err);
        } else if (err instanceof Error) {
          Logger.log(err.message);
        }
      }
      return Promise.reject(new Error("Failed to retrieve app properties"));
  }
}
