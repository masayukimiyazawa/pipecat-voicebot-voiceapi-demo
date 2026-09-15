```mermaid
graph TB
    Input["Transport Input<br/>WebSocket Input"]
    
    Log["AudioFrameLogger<br/>Debug Logging"]
    
    VAD["VADProcessor<br/>SileroVAD<br/>confidence=0.5<br/>start=0.2s stop=0.2s"]
    
    STT["WhisperSTTServiceMLX<br/>Language: ja<br/>Model: LARGE_V3_TURBO_Q4"]
    
    UserAgg["LLMUserAggregator<br/>Add to Conversation<br/>timeout=5.0s"]
    
    LLM["OpenAILLMService<br/>Base URL: localhost:1234/v1<br/>System Prompt: Japanese"]
    
    AssAgg["LLMAssistantAggregator<br/>Monkey-patch Applied<br/>Forward TextFrame Downstream"]
    
    TTS["PiperPlusTTSService<br/>pyopenjtalk<br/>Speed: 1.0 Pitch: 0.0<br/>Chunk: 4096B"]
    
    Output["Transport Output<br/>WebSocket Output"]
    
    Context["LLMContext<br/>Message Management"]
    
    Input --> Log
    Log --> VAD
    VAD --> STT
    STT --> UserAgg
    UserAgg --> Context
    Context --> LLM
    LLM --> AssAgg
    AssAgg --> Context
    Context --> TTS
    TTS --> Output
    
    style Input fill:#e3f2fd,stroke:#1565c0
    style Output fill:#c8e6c9,stroke:#2e7d32
    style Context fill:#fff9c4,stroke:#f57f17
    style VAD fill:#bbdefb,stroke:#1565c0
    style STT fill:#c5cae9,stroke:#283593
    style LLM fill:#fff3e0,stroke:#e65100
    style TTS fill:#f8bbd0,stroke:#c2185b
```
