package com.example.demo;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import org.springframework.beans.factory.annotation.Autowired;

@RestController
@RequestMapping("/api/review")
@CrossOrigin(origins = "http://localhost:5173")
public class CodeReviewController {

    private final RestTemplate restTemplate;

    @Autowired
    public CodeReviewController(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    @PostMapping
    public ResponseEntity<String> reviewCode(@RequestBody String code) {
        // Call AI service
        String aiUrl = "http://localhost:5000/review"; // Assuming Python service runs on 5000
        ResponseEntity<String> response = restTemplate.postForEntity(aiUrl, code, String.class);
        return response;
    }
}