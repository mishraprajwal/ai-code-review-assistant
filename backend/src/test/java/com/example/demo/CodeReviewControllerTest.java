package com.example.demo;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class CodeReviewControllerTest {

    @Mock
    private RestTemplate restTemplate;

    @InjectMocks
    private CodeReviewController controller;

    @Test
    void testReviewCode_Success() {
        // Arrange
        String code = "public class Test { }";
        String expectedFeedback = "{\"feedback\":\"Good code\"}";
        ResponseEntity<String> mockResponse = new ResponseEntity<>(expectedFeedback, HttpStatus.OK);
        when(restTemplate.postForEntity(eq("http://localhost:5000/review"), eq(code), eq(String.class)))
                .thenReturn(mockResponse);

        // Act
        ResponseEntity<String> response = controller.reviewCode(code);

        // Assert
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(expectedFeedback, response.getBody());
    }

    @Test
    void testReviewCode_AIServiceError() {
        // Arrange
        String code = "invalid code";
        ResponseEntity<String> mockResponse = new ResponseEntity<>("Error", HttpStatus.INTERNAL_SERVER_ERROR);
        when(restTemplate.postForEntity(any(String.class), any(String.class), eq(String.class)))
                .thenReturn(mockResponse);

        // Act
        ResponseEntity<String> response = controller.reviewCode(code);

        // Assert
        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
        assertEquals("Error", response.getBody());
    }
}