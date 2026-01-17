# Voice Testing Guide

## Overview

This guide provides comprehensive testing procedures for the voice input and voice output features of the Todo AI Chatbot.

## Prerequisites

- **Browser**: Chrome (recommended), Edge, or Safari
- **Microphone**: Working microphone with permissions granted
- **Speakers**: Working audio output
- **Environment**: HTTPS connection (required for some browsers)

## Browser Compatibility

| Browser | Voice Input | Voice Output | Notes |
|---------|-------------|--------------|-------|
| Chrome | ✅ Full Support | ✅ Full Support | Best experience |
| Edge | ✅ Full Support | ✅ Full Support | Chromium-based |
| Safari | ⚠️ Limited | ✅ Full Support | May require user gesture |
| Firefox | ❌ No Support | ✅ Full Support | Web Speech API not supported |

## Voice Input Testing

### Test 1: Basic Voice Recognition

**Objective**: Verify voice input captures speech correctly

**Steps**:
1. Open http://localhost:3000/chatbot
2. Navigate to the **Chat** tab
3. Click the 🎤 microphone button
4. Verify the button turns red and shows "🔴"
5. Verify the text "🎤 Listening... Speak now" appears below the input
6. Speak clearly: "Add a task to buy groceries"
7. Wait for recognition to complete
8. Verify the text appears in the input field
9. Click "Send" button
10. Verify the task is created

**Expected Results**:
- ✅ Microphone button changes to red when listening
- ✅ Visual feedback shows "Listening..."
- ✅ Speech is transcribed to text accurately
- ✅ Text appears in input field
- ✅ Task is created successfully

**Common Issues**:
- **No transcription**: Check microphone permissions
- **Inaccurate transcription**: Speak more clearly, reduce background noise
- **Button doesn't activate**: Check browser compatibility

### Test 2: Multiple Voice Commands

**Objective**: Test various voice commands

**Test Cases**:

| Command | Expected Result |
|---------|----------------|
| "Add a task to call mom" | Task created with title "Call mom" |
| "Show me all my tasks" | List of tasks displayed |
| "Mark task 1 as complete" | Task 1 marked as completed |
| "Create a daily recurring task for standup" | Recurring task created |
| "Delete task 2" | Task 2 deleted |
| "Update task 3 to buy milk and eggs" | Task 3 title updated |

**Steps for each command**:
1. Click microphone button
2. Speak the command
3. Wait for transcription
4. Send message
5. Verify expected result

### Test 3: Voice Input Error Handling

**Objective**: Test error scenarios

**Test Cases**:

1. **No Speech Detected**:
   - Click microphone
   - Wait 5 seconds without speaking
   - Verify: Recognition stops, no error shown

2. **Background Noise**:
   - Click microphone
   - Play background music
   - Speak command
   - Verify: May have reduced accuracy but still works

3. **Microphone Permission Denied**:
   - Deny microphone permission
   - Click microphone button
   - Verify: Error message or button disabled

4. **Unsupported Browser**:
   - Open in Firefox
   - Verify: Microphone button hidden or disabled

## Voice Output Testing

### Test 4: Basic Text-to-Speech

**Objective**: Verify voice output reads responses

**Steps**:
1. Open http://localhost:3000/chatbot
2. Navigate to the **Chat** tab
3. Type message: "What are my pending tasks?"
4. Click "Send"
5. Wait for assistant response
6. Verify: Response is read aloud automatically
7. Verify: "🔊 Speaking..." indicator appears
8. Wait for speech to complete
9. Verify: Indicator disappears when done

**Expected Results**:
- ✅ Response is spoken clearly
- ✅ Visual indicator shows speaking status
- ✅ Speech completes without interruption
- ✅ Indicator disappears when done

### Test 5: Voice Output Control

**Objective**: Test voice output can be controlled

**Steps**:
1. Send a message that generates a long response
2. While speaking, observe the "🔊 Speaking..." indicator
3. Test stopping speech (if stop button implemented)
4. Verify speech stops immediately

**Note**: Current implementation auto-speaks responses. Future enhancement could add toggle control.

### Test 6: Multiple Responses

**Objective**: Test sequential voice outputs

**Steps**:
1. Send message: "Show me all my tasks"
2. Wait for response to be spoken
3. Immediately send: "How many tasks do I have?"
4. Verify: Previous speech stops, new speech starts
5. Verify: No overlap or audio conflicts

## Integration Testing

### Test 7: Voice-to-Voice Workflow

**Objective**: Complete task management using only voice

**Scenario**: Create, list, complete, and delete a task using voice

**Steps**:
1. **Create Task**:
   - Click microphone
   - Say: "Add a task to test voice features"
   - Verify: Task created, confirmation spoken

2. **List Tasks**:
   - Click microphone
   - Say: "Show me all my tasks"
   - Verify: Tasks listed, response spoken

3. **Complete Task**:
   - Click microphone
   - Say: "Mark the test task as complete"
   - Verify: Task completed, confirmation spoken

4. **Delete Task**:
   - Click microphone
   - Say: "Delete the test task"
   - Verify: Task deleted, confirmation spoken

**Expected Results**:
- ✅ All operations complete successfully
- ✅ All responses are spoken
- ✅ No manual typing required
- ✅ Workflow is smooth and natural

### Test 8: Voice + Analytics

**Objective**: Use voice to query analytics

**Steps**:
1. Create 5 tasks (3 completed, 2 pending)
2. Click microphone
3. Say: "Show me my task statistics"
4. Verify: Agent provides statistics
5. Navigate to Analytics tab
6. Verify: Charts match spoken statistics

### Test 9: Voice + Recurring Tasks

**Objective**: Create recurring task via voice

**Steps**:
1. Click microphone
2. Say: "Create a daily recurring task for morning standup"
3. Verify: Recurring task created
4. Navigate to Recurring tab
5. Verify: Task appears in list

## Performance Testing

### Test 10: Voice Recognition Latency

**Objective**: Measure voice recognition speed

**Steps**:
1. Click microphone
2. Say: "Add a task"
3. Measure time from end of speech to text appearance
4. Record latency

**Acceptable Latency**:
- ✅ < 1 second: Excellent
- ⚠️ 1-3 seconds: Acceptable
- ❌ > 3 seconds: Poor (check network/browser)

### Test 11: Voice Output Latency

**Objective**: Measure text-to-speech delay

**Steps**:
1. Send message
2. Measure time from response display to speech start
3. Record latency

**Acceptable Latency**:
- ✅ < 500ms: Excellent
- ⚠️ 500ms-1s: Acceptable
- ❌ > 1s: Poor (check browser)

## Accessibility Testing

### Test 12: Keyboard Navigation

**Objective**: Verify voice features are keyboard accessible

**Steps**:
1. Use Tab key to navigate to microphone button
2. Press Enter to activate
3. Speak command
4. Verify: Works same as mouse click

### Test 13: Screen Reader Compatibility

**Objective**: Test with screen reader

**Steps**:
1. Enable screen reader (NVDA, JAWS, VoiceOver)
2. Navigate to chat interface
3. Verify: Microphone button is announced
4. Verify: Listening status is announced
5. Verify: Responses are read by screen reader

## Privacy & Security Testing

### Test 14: Microphone Permission

**Objective**: Verify proper permission handling

**Steps**:
1. First visit: Verify permission prompt appears
2. Grant permission: Verify microphone works
3. Revoke permission: Verify graceful degradation
4. Re-grant permission: Verify microphone works again

### Test 15: Data Privacy

**Objective**: Verify voice data is not stored

**Steps**:
1. Use voice input
2. Check browser console for network requests
3. Verify: No audio data sent to server
4. Verify: Only transcribed text sent to backend

## Troubleshooting Guide

### Issue: Microphone Not Working

**Symptoms**: No transcription, button doesn't activate

**Solutions**:
1. Check browser permissions (chrome://settings/content/microphone)
2. Verify microphone is connected and working
3. Try different browser (Chrome recommended)
4. Check for HTTPS connection
5. Restart browser

### Issue: Inaccurate Transcription

**Symptoms**: Wrong words, gibberish

**Solutions**:
1. Speak more clearly and slowly
2. Reduce background noise
3. Move closer to microphone
4. Check microphone quality
5. Try different microphone

### Issue: Voice Output Not Working

**Symptoms**: No speech, silent responses

**Solutions**:
1. Check system volume
2. Check browser audio permissions
3. Verify speakers are working
4. Try different browser
5. Check browser console for errors

### Issue: Voice Cuts Off

**Symptoms**: Speech stops mid-sentence

**Solutions**:
1. Check network connection
2. Verify browser supports Web Speech API
3. Update browser to latest version
4. Clear browser cache
5. Try incognito mode

## Test Results Template

Use this template to record test results:

```markdown
## Test Session: [Date]

**Tester**: [Name]
**Browser**: [Chrome/Edge/Safari] [Version]
**OS**: [Windows/Mac/Linux]

### Voice Input Tests
- [ ] Test 1: Basic Recognition - PASS/FAIL
- [ ] Test 2: Multiple Commands - PASS/FAIL
- [ ] Test 3: Error Handling - PASS/FAIL

### Voice Output Tests
- [ ] Test 4: Basic TTS - PASS/FAIL
- [ ] Test 5: Output Control - PASS/FAIL
- [ ] Test 6: Multiple Responses - PASS/FAIL

### Integration Tests
- [ ] Test 7: Voice-to-Voice - PASS/FAIL
- [ ] Test 8: Voice + Analytics - PASS/FAIL
- [ ] Test 9: Voice + Recurring - PASS/FAIL

### Performance Tests
- [ ] Test 10: Recognition Latency - [X]ms
- [ ] Test 11: Output Latency - [X]ms

### Accessibility Tests
- [ ] Test 12: Keyboard Navigation - PASS/FAIL
- [ ] Test 13: Screen Reader - PASS/FAIL

### Privacy Tests
- [ ] Test 14: Permissions - PASS/FAIL
- [ ] Test 15: Data Privacy - PASS/FAIL

**Issues Found**: [List any issues]
**Notes**: [Additional observations]
```

## Automated Testing (Future)

For automated voice testing, consider:
- Puppeteer with audio injection
- Selenium with speech synthesis mocking
- Jest with Web Speech API mocks
- Cypress with audio testing plugins

## Conclusion

Voice features are critical for accessibility and user experience. Regular testing ensures they work reliably across browsers and scenarios.

**Next Steps**:
1. Complete all manual tests
2. Document any issues
3. Fix critical bugs
4. Consider automated testing
5. Monitor user feedback

---

**Last Updated**: 2026-01-10
**Version**: 1.0
**Status**: Ready for Testing
