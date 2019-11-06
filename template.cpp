#include "catch/catch2"

{% for scenario in scenarios %}
SCENARIO("{{ scenario.name }}", "[{{ scenario.tag }}]") {
    {% for test in scenario.tests %}
    GIVEN("{{ test.given }}") {
        {% for when in test.whens %}
        WHEN("{{ when }}") {
            {% for then in test.thens %}
            THEN("{{ then }}") {
            }
            {% endfor %}
        }
        {% endfor %}
    }
    {% endfor %}
}
{% endfor %}