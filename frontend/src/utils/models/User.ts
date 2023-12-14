export default interface User {
  id: number;
  username: string;
  date_of_birth: Date;
  email: string;
  profile_picture: string;
  preferences: string[];
}