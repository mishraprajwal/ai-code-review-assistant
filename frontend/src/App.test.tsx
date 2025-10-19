import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { vi } from 'vitest'
import App from './App'

// Mock fetch
const mockFetch = vi.fn();
global.fetch = mockFetch;

describe('App', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  test('renders the app title', () => {
    render(<App />)
    expect(screen.getByText('AI Code Review Assistant')).toBeInTheDocument()
  })

  test('renders textarea and button', () => {
    render(<App />)
    expect(screen.getByPlaceholderText('Enter your code...')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /review code/i })).toBeInTheDocument()
  })

  test('submits code and displays feedback', async () => {
    const mockResponse = { feedback: 'Good code!' }
    mockFetch.mockResolvedValueOnce({
      json: () => Promise.resolve(mockResponse)
    } as Response)

    render(<App />)
    const textarea = screen.getByPlaceholderText('Enter your code...')
    const button = screen.getByRole('button', { name: /review code/i })

    fireEvent.change(textarea, { target: { value: 'def test(): pass' } })
    fireEvent.click(button)

    await waitFor(() => {
      expect(screen.getByText('Good code!')).toBeInTheDocument()
    })
  })

  test('handles fetch error', async () => {
    mockFetch.mockRejectedValueOnce(new Error('Network error'))

    render(<App />)
    const textarea = screen.getByPlaceholderText('Enter your code...')
    const button = screen.getByRole('button', { name: /review code/i })

    fireEvent.change(textarea, { target: { value: 'def test(): pass' } })
    fireEvent.click(button)

    await waitFor(() => {
      expect(screen.getByText('Error: Unable to get review.')).toBeInTheDocument()
    })
  })
})