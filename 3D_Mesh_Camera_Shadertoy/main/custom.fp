varying highp vec3 var_position;

void main()
{
    gl_FragColor = vec4((var_position.xy + 1.0) * 0.5, 0.0, 1.0);
}

