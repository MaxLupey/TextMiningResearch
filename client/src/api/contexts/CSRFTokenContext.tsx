import { createContext } from 'react';

export const CSRFTokenContext = createContext<string | null>(null);