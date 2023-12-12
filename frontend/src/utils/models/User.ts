export default interface User {
  id: number;
  username: string;
  date_of_birth: Date;
  email: String;
  preferences: Array<String>;
  // TODO: WEB-9 do we need any more fields in User here?
}