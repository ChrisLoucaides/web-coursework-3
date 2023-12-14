export default interface User {
  id: number;
  username: string;
  date_of_birth: Date;
  email: String;
  profile_picture: File;
  preferences: string[];
}