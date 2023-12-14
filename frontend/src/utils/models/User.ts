export default interface User {
  id: number;
  username: string;
  date_of_birth: Date;
  email: String;
  profile_picture: File;
  preferences: string[];
  // TODO: WEB-9 do we need any more fields in User here?
}