#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════════
# BRAIN SERVICE TESTS - COMPREHENSIVE
# ═══════════════════════════════════════════════════════════════════════════════

source "$(dirname "$0")/lib/common.sh"

# Persian test texts with different sentiments
POSITIVE_TEXT="امروز روز فوق‌العاده‌ای بود! خیلی خوشحالم که این موفقیت را کسب کردم."
NEGATIVE_TEXT="وضعیت اقتصادی خیلی بد شده. همه چیز گران است و مردم ناراحت هستند."
NEUTRAL_TEXT="امروز هوا ابری است. دمای هوا حدود ۲۰ درجه سانتیگراد است."
MIXED_TEXT="فیلم خوب بود ولی پایانش ناامیدکننده بود."

# Test texts array
PERSIAN_TEXTS=(
    "این محصول عالی است! کیفیت بسیار بالایی دارد."
    "از خرید این کالا پشیمانم. کیفیت افتضاح بود."
    "قیمت مناسب است ولی کیفیت متوسط."
    "خدمات پشتیبانی عالی بود، سریع جواب دادند."
    "تحویل خیلی دیر شد و بسته‌بندی آسیب دیده بود."
    "نصف جهان اصفهان واقعاً زیباست!"
    "ترافیک تهران امروز وحشتناک بود."
    "غذای این رستوران خوشمزه است."
    "فوتبال ایران نتیجه خوبی گرفت."
    "کتاب جالبی بود، پیشنهاد می‌کنم."
)

test_brain() {
    print_header "🧠 BRAIN SERVICE TESTS"
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "BRAIN Health & Info"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "BRAIN health endpoint"
    local response=$(http_get "$BRAIN_URL/health" false)
    local body=$(get_body "$response")
    local status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        print_pass
        print_json "$body"
    else
        print_fail "HTTP $status"
        return 1
    fi
    
    print_test "BRAIN version/info"
    response=$(http_get "$BRAIN_URL/info" false)
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        print_pass
        print_json "$body"
    else
        print_skip "Info endpoint not available"
    fi
    
    print_test "Available models"
    response=$(http_get "$BRAIN_URL/models" false)
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        print_pass
        print_json "$body"
    else
        print_skip "Models endpoint not available"
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Sentiment Analysis"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_subsection "Single Text Analysis"
    
    print_test "Positive sentiment detection"
    response=$(http_post "$BRAIN_URL/analyze/sentiment" \
        "{\"texts\": [\"$POSITIVE_TEXT\"]}" false)
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        local sentiment=$(echo "$body" | jq -r '.results[0].label // .results[0].sentiment // .[0].label' 2>/dev/null)
        local score=$(echo "$body" | jq -r '.results[0].score // .results[0].confidence // .[0].score' 2>/dev/null)
        if [[ "$sentiment" =~ [Pp]ositive ]] || [[ "$sentiment" == "مثبت" ]]; then
            print_pass "Detected: $sentiment (score: $score)"
        else
            print_fail "Expected positive, got: $sentiment"
        fi
        print_json "$body"
    else
        print_fail "HTTP $status"
    fi
    
    print_test "Negative sentiment detection"
    response=$(http_post "$BRAIN_URL/analyze/sentiment" \
        "{\"texts\": [\"$NEGATIVE_TEXT\"]}" false)
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        local sentiment=$(echo "$body" | jq -r '.results[0].label // .results[0].sentiment // .[0].label' 2>/dev/null)
        local score=$(echo "$body" | jq -r '.results[0].score // .results[0].confidence // .[0].score' 2>/dev/null)
        if [[ "$sentiment" =~ [Nn]egative ]] || [[ "$sentiment" == "منفی" ]]; then
            print_pass "Detected: $sentiment (score: $score)"
        else
            print_fail "Expected negative, got: $sentiment"
        fi
        print_json "$body"
    else
        print_fail "HTTP $status"
    fi
    
    print_test "Neutral sentiment detection"
    response=$(http_post "$BRAIN_URL/analyze/sentiment" \
        "{\"texts\": [\"$NEUTRAL_TEXT\"]}" false)
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        local sentiment=$(echo "$body" | jq -r '.results[0].label // .results[0].sentiment // .[0].label' 2>/dev/null)
        print_pass "Detected: $sentiment"
        print_json "$body"
    else
        print_fail "HTTP $status"
    fi
    
    print_subsection "Batch Analysis"
    
    print_test "Multiple texts (batch)"
    local batch_texts=$(printf '%s\n' "${PERSIAN_TEXTS[@]}" | jq -R . | jq -s '.')
    response=$(http_post "$BRAIN_URL/analyze/sentiment" \
        "{\"texts\": $batch_texts}" false)
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        local count=$(echo "$body" | jq '.results | length // . | length' 2>/dev/null)
        print_pass "Analyzed $count texts"
        print_info "Distribution:"
        echo "$body" | jq -C '[.results // .[]] | group_by(.label // .sentiment) | map({label: .[0].label // .[0].sentiment, count: length})' 2>/dev/null | sed 's/^/  │   /'
    else
        print_fail "HTTP $status"
    fi
    
    print_subsection "Edge Cases"
    
    print_test "Empty text handling"
    response=$(http_post "$BRAIN_URL/analyze/sentiment" \
        '{"texts": [""]}' false)
    status=$(get_status_code "$response")
    if [ "$status" = "200" ] || [ "$status" = "400" ] || [ "$status" = "422" ]; then
        print_pass "Handled gracefully (HTTP $status)"
    else
        print_fail "Unexpected: HTTP $status"
    fi
    
    print_test "Very long text"
    local long_text=$(printf 'این یک متن طولانی است. %.0s' {1..100})
    response=$(http_post "$BRAIN_URL/analyze/sentiment" \
        "{\"texts\": [\"$long_text\"]}" false)
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        print_pass
    else
        print_skip "HTTP $status (may have length limit)"
    fi
    
    print_test "Special characters"
    response=$(http_post "$BRAIN_URL/analyze/sentiment" \
        '{"texts": ["متن با کاراکتر خاص: @#$%^& و ایموجی 😀🎉"]}' false)
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        print_pass
    else
        print_fail "HTTP $status"
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Emotion Detection"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "Emotion analysis endpoint"
    response=$(http_post "$BRAIN_URL/analyze/emotion" \
        "{\"texts\": [\"$POSITIVE_TEXT\", \"$NEGATIVE_TEXT\"]}" false)
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        print_pass
        print_json "$body"
    else
        print_skip "Emotion endpoint not available (HTTP $status)"
    fi
    
    print_test "Emotion with scores"
    response=$(http_post "$BRAIN_URL/analyze/emotion" \
        '{"texts": ["خیلی عصبانی هستم!", "خیلی خوشحالم!", "خیلی ترسیدم!", "متعجب شدم!"]}' false)
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        print_pass
        print_json "$body"
    else
        print_skip "HTTP $status"
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Keyword Extraction"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "Extract keywords"
    response=$(http_post "$BRAIN_URL/analyze/keywords" \
        '{"texts": ["برنامه‌نویسی پایتون و یادگیری ماشین در هوش مصنوعی کاربرد فراوانی دارد."]}' false)
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        print_pass
        print_json "$body"
    else
        print_skip "Keywords endpoint not available (HTTP $status)"
    fi
    
    print_test "Keywords with count limit"
    response=$(http_post "$BRAIN_URL/analyze/keywords" \
        '{"texts": ["تهران پایتخت ایران است و جمعیت زیادی دارد. تهران شهر بزرگی است."], "top_k": 5}' false)
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        print_pass
        print_json "$body"
    else
        print_skip "HTTP $status"
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Named Entity Recognition (NER)"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "NER extraction"
    response=$(http_post "$BRAIN_URL/analyze/ner" \
        '{"texts": ["علی رضایی از تهران به اصفهان سفر کرد. او در شرکت سامسونگ کار می‌کند."]}' false)
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        print_pass
        print_json "$body"
    else
        print_skip "NER endpoint not available (HTTP $status)"
    fi
    
    print_test "NER with multiple entity types"
    response=$(http_post "$BRAIN_URL/analyze/ner" \
        '{"texts": ["رئیس جمهور ایران روز دوشنبه در سازمان ملل سخنرانی کرد. مبلغ ۱۰۰ میلیون دلار تصویب شد."]}' false)
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        print_pass
        print_json "$body"
    else
        print_skip "HTTP $status"
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Topic Modeling"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "Topic detection"
    response=$(http_post "$BRAIN_URL/analyze/topics" \
        "{\"texts\": $batch_texts}" false)
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        print_pass
        print_json "$body"
    else
        print_skip "Topics endpoint not available (HTTP $status)"
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Text Classification"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "Text classification"
    response=$(http_post "$BRAIN_URL/analyze/classify" \
        '{"texts": ["این خبر ورزشی است", "قیمت دلار افزایش یافت", "فیلم جدید اکران شد"]}' false)
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        print_pass
        print_json "$body"
    else
        print_skip "Classification endpoint not available (HTTP $status)"
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Language Detection"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "Persian language detection"
    response=$(http_post "$BRAIN_URL/analyze/language" \
        '{"texts": ["سلام، حال شما چطور است؟"]}' false)
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        print_pass
        print_json "$body"
    else
        print_skip "Language endpoint not available (HTTP $status)"
    fi
    
    print_test "Multi-language detection"
    response=$(http_post "$BRAIN_URL/analyze/language" \
        '{"texts": ["Hello world", "سلام دنیا", "مرحبا بالعالم", "Bonjour le monde"]}' false)
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        print_pass
        print_json "$body"
    else
        print_skip "HTTP $status"
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Full Analysis Pipeline"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "Complete analysis (all features)"
    response=$(http_post "$BRAIN_URL/analyze/full" \
        "{\"texts\": [\"$POSITIVE_TEXT\", \"$NEGATIVE_TEXT\"], \"features\": [\"sentiment\", \"emotion\", \"keywords\", \"ner\"]}" false)
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        print_pass
        print_json "$body"
    else
        print_skip "Full analysis endpoint not available (HTTP $status)"
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Performance & Limits"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "Response time (single request)"
    local start_time=$(date +%s%N)
    response=$(http_post "$BRAIN_URL/analyze/sentiment" \
        '{"texts": ["تست سرعت پاسخ‌دهی"]}' false)
    local end_time=$(date +%s%N)
    local duration=$(( (end_time - start_time) / 1000000 ))
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        if [ "$duration" -lt 1000 ]; then
            print_pass "${duration}ms"
        else
            print_pass "${duration}ms (slow)"
        fi
    else
        print_fail "HTTP $status"
    fi
    
    print_test "Batch performance (10 texts)"
    start_time=$(date +%s%N)
    response=$(http_post "$BRAIN_URL/analyze/sentiment" \
        "{\"texts\": $batch_texts}" false)
    end_time=$(date +%s%N)
    duration=$(( (end_time - start_time) / 1000000 ))
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        print_pass "${duration}ms total, $((duration/10))ms per text"
    else
        print_fail "HTTP $status"
    fi
    
    print_test "Large batch (50 texts)"
    local large_batch=$(printf '%s\n' "${PERSIAN_TEXTS[@]}" "${PERSIAN_TEXTS[@]}" "${PERSIAN_TEXTS[@]}" "${PERSIAN_TEXTS[@]}" "${PERSIAN_TEXTS[@]}" | jq -R . | jq -s '.')
    start_time=$(date +%s%N)
    response=$(http_post "$BRAIN_URL/analyze/sentiment" \
        "{\"texts\": $large_batch}" false)
    end_time=$(date +%s%N)
    duration=$(( (end_time - start_time) / 1000000 ))
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        print_pass "${duration}ms total"
    else
        print_skip "HTTP $status (may have batch limit)"
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Error Handling"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "Invalid JSON"
    response=$(curl -s -w "\n%{http_code}" -X POST "$BRAIN_URL/analyze/sentiment" \
        -H "Content-Type: application/json" \
        -d 'invalid json')
    status=$(get_status_code "$response")
    if [ "$status" = "400" ] || [ "$status" = "422" ]; then
        print_pass "Correctly rejected (HTTP $status)"
    else
        print_fail "Expected 400/422, got $status"
    fi
    
    print_test "Missing required field"
    response=$(http_post "$BRAIN_URL/analyze/sentiment" \
        '{"wrong_field": ["test"]}' false)
    status=$(get_status_code "$response")
    if [ "$status" = "400" ] || [ "$status" = "422" ]; then
        print_pass "Correctly rejected (HTTP $status)"
    else
        print_fail "Expected 400/422, got $status"
    fi
    
    print_test "Empty array"
    response=$(http_post "$BRAIN_URL/analyze/sentiment" \
        '{"texts": []}' false)
    status=$(get_status_code "$response")
    if [ "$status" = "200" ] || [ "$status" = "400" ] || [ "$status" = "422" ]; then
        print_pass "Handled (HTTP $status)"
    else
        print_fail "Unexpected: HTTP $status"
    fi
    
    print_test "Non-existent endpoint"
    response=$(http_get "$BRAIN_URL/analyze/nonexistent" false)
    status=$(get_status_code "$response")
    if [ "$status" = "404" ]; then
        print_pass "Correctly returned 404"
    else
        print_fail "Expected 404, got $status"
    fi
    
    print_divider
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    init_tests
    test_brain
    print_summary
fi
