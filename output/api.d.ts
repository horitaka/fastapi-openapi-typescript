export type GetUsersResponse = {
  users?: (User)[];
};

export type HTTPValidationError = {
  detail?: (ValidationError)[];
};

export type PostUsersRequest = {
  name: string;
  email: string;
};

export type User = {
  id: number;
  name: string;
  email: string;
  address?: string | null;
};

export type ValidationError = {
  loc: (string | number)[];
  msg: string;
  type: string;
};
