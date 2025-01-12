from typing import Any

import aws_cdk as cdk
import aws_cdk.aws_cognito as cognito
from constructs import Construct


class ServiceStack(cdk.Stack):
    def __init__(self, scope: Construct, id_: str, **kwargs: Any):
        super().__init__(scope, id_, **kwargs)

        cognito_userpool = cognito.UserPool(
            self,
            "CognitoUserPool",
            custom_attributes={
                "role": cognito.StringAttribute(),
                "tenant_id": cognito.StringAttribute(),
            },
            removal_policy=cdk.RemovalPolicy.DESTROY,
            sign_in_aliases=cognito.SignInAliases(email=True, username=False),
            sign_in_case_sensitive=False,
        )
        cognito_userpool_domain = cognito_userpool.add_domain(
            "Domain",
            cognito_domain=cognito.CognitoDomainOptions(
                domain_prefix=f"{cdk.Stack.of(self).account}-example",
            ),
        )
        ui_app_sign_in_url = self._create_ui_cognito_app_client(
            cognito_userpool, cognito_userpool_domain
        )

        cdk.CfnOutput(
            self,
            "CognitoUserPoolID",
            value=cognito_userpool.user_pool_id,
        )
        cdk.CfnOutput(
            self,
            "UIAppSignInURL",
            value=ui_app_sign_in_url,
        )

    def _create_ui_cognito_app_client(
        self,
        cognito_userpool: cognito.UserPool,
        cognito_userpool_domain: cognito.UserPoolDomain,
    ) -> str:
        cognito_app_client_name = "UI"
        ui_app_url = (
            f"https://{cognito_app_client_name.lower()}.{cdk.Stack.of(self).region}."
            f"{cdk.Stack.of(self).account}.product.example.com"
        )
        ui_cognito_app_client = cognito_userpool.add_client(
            cognito_app_client_name,
            o_auth=cognito.OAuthSettings(
                callback_urls=[ui_app_url, "http://localhost"],
                flows=cognito.OAuthFlows(implicit_code_grant=True),
                logout_urls=[ui_app_url],
                scopes=[cognito.OAuthScope.OPENID],
            ),
        )
        ui_app_sign_in_url = cognito_userpool_domain.sign_in_url(
            ui_cognito_app_client,
            redirect_uri=ui_app_url,
        )
        return ui_app_sign_in_url
