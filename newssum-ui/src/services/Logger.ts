export default class NewsSumApi {
  static log(message: string, level?: 'info' | 'warn' | 'error') {
    if (import.meta.env.DEV) {
         
        if (level === 'error') {
            console.error(message);
        } else if (level === 'warn') {
            console.warn(message);
        } else {
            console.log(message);
        }
         
    }
  }
}
