export default class NewsSumApi {
  static log(message: String, level?: 'info' | 'warn' | 'error') {
    if (import.meta.env.DEV) {
        /* eslint-disable no-console */
        if (level === 'error') {
            console.error(message);
        } else if (level === 'warn') {
            console.warn(message);
        } else {
            console.log(message);
        }
        /* eslint-enable no-console */
    }
  }
}
